"""Install a presentation-only zone overlay into the real PipeGen export.

The Python MVC model still owns incident decisions. This extension only adds
NvDsDisplayMeta for nvdsosd to draw the same configured polygons on real frames.
"""
import argparse
import json
from pathlib import Path
from guardianedge.models.zones import ZoneEngine


def install(export_root, configuration):
    config = json.loads(Path(configuration).read_text(encoding='utf-8'))
    model = ZoneEngine(config['zones'], config.get('confirm_frames', 3), config.get('min_confidence', .5))
    if any(len(polygon) > 16 for _, polygon in model.zones):
        raise ValueError('overlay currently supports at most 16 vertices per zone')
    parsers = Path(export_root) / 'pipeline' / 'parsers'
    source = parsers / 'meta_json.cpp'
    content = source.read_text(encoding='utf-8')
    marker = '    NvDsFrameMeta* fm = (NvDsFrameMeta*) in->frame_meta;'
    if marker not in content:
        raise ValueError('unexpected vendor extension interface; inspect source before patching')
    header = ['// GuardianEdge MVC view extension, generated from zone configuration.',
              '#pragma once', '#include "nvdsmeta.h"', '#include <glib.h>',
              'inline void guardianedge_zone(NvDsFrameMeta* fm, int width, int height) {',
              '  if (!fm || !fm->base_meta.batch_meta) return;']
    for zid, polygon in model.zones:
        points = ','.join('{'+str(x)+','+str(y)+'}' for x, y in polygon)
        label = json.dumps('GuardianEdge DEMO zone: ' + zid)
        header += ['  {', '    const double points[][2] = {'+points+'};',
                   '    NvDsDisplayMeta* display = nvds_acquire_display_meta_from_pool(fm->base_meta.batch_meta);',
                   '    if (!display) return;', f'    display->num_lines = {len(polygon)};',
                   f'    for (unsigned i=0; i<{len(polygon)}; ++i) {{',
                   f'      unsigned j = (i+1)%{len(polygon)};',
                   '      auto& line = display->line_params[i];',
                   '      line.x1=points[i][0]*width; line.y1=points[i][1]*height;',
                   '      line.x2=points[j][0]*width; line.y2=points[j][1]*height;',
                   '      line.line_width=3; line.line_color={1.0,0.7,0.0,1.0};', '    }',
                   '    display->num_labels=1;', '    auto& text=display->text_params[0];',
                   '    text.display_text=g_strdup('+label+');',
                   '    text.x_offset=20; text.y_offset=30;',
                   '    text.font_params.font_name=(char*)"Sans"; text.font_params.font_size=16;',
                   '    text.font_params.font_color={1.0,1.0,1.0,1.0};',
                   '    text.set_bg_clr=1; text.text_bg_clr={0.0,0.0,0.0,0.8};',
                   '    nvds_add_display_meta_to_frame(fm,display);', '  }']
    header += ['}']
    (parsers/'guardianedge_zone.h').write_text('\n'.join(header)+'\n', encoding='utf-8')
    if '#include "guardianedge_zone.h"' not in content:
        content = content.replace('#include "frame_json.h"', '#include "frame_json.h"\n#include "guardianedge_zone.h"', 1)
        content = content.replace(marker, marker+'\n    if (fm) guardianedge_zone(fm, in->W, in->H);', 1)
        source.write_text(content, encoding='utf-8')
    makefile = parsers/'Makefile'
    rules = makefile.read_text()
    rules = rules.replace('libmeta_json.so: meta_json.cpp frame_json.h render_meta.h Makefile',
                          'libmeta_json.so: meta_json.cpp frame_json.h render_meta.h guardianedge_zone.h Makefile')
    makefile.write_text(rules)
    print(f'Installed zone presentation extension in {parsers}')


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--export', required=True)
    parser.add_argument('--config', required=True)
    args=parser.parse_args()
    install(args.export, args.config)
