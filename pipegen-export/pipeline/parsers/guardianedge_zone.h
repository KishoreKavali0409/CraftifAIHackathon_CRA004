// GuardianEdge MVC view extension, generated from zone configuration.
#pragma once
#include "nvdsmeta.h"
#include <glib.h>
inline void guardianedge_zone(NvDsFrameMeta* fm, int width, int height) {
  if (!fm || !fm->base_meta.batch_meta) return;
  {
    const double points[][2] = {{0.04,0.45},{0.28,0.45},{0.28,0.95},{0.04,0.95}};
    NvDsDisplayMeta* display = nvds_acquire_display_meta_from_pool(fm->base_meta.batch_meta);
    if (!display) return;
    display->num_lines = 4;
    for (unsigned i=0; i<4; ++i) {
      unsigned j = (i+1)%4;
      auto& line = display->line_params[i];
      line.x1=points[i][0]*width; line.y1=points[i][1]*height;
      line.x2=points[j][0]*width; line.y2=points[j][1]*height;
      line.line_width=3; line.line_color={1.0,0.7,0.0,1.0};
    }
    display->num_labels=1;
    auto& text=display->text_params[0];
    text.display_text=g_strdup("GuardianEdge DEMO zone: demo-walkway-A");
    text.x_offset=20; text.y_offset=30;
    text.font_params.font_name=(char*)"Sans"; text.font_params.font_size=16;
    text.font_params.font_color={1.0,1.0,1.0,1.0};
    text.set_bg_clr=1; text.text_bg_clr={0.0,0.0,0.0,0.8};
    nvds_add_display_meta_to_frame(fm,display);
  }
}
