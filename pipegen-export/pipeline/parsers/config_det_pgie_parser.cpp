// Custom detection (bbox) parser (generated).
// Scaffold validates the output layer and exposes the raw tensor(s); the DECODE
// block (per-model) populates `objectList` with NvDsInferObjectDetectionInfo.
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <string>
#include <vector>

#include "nvdsinfer_custom_impl.h"

extern "C" bool ParseConfigDetPgie(
    std::vector<NvDsInferLayerInfo> const& outputLayersInfo,
    NvDsInferNetworkInfo const& networkInfo,
    NvDsInferParseDetectionParams const& detectionParams,
    std::vector<NvDsInferObjectDetectionInfo>& objectList);

CHECK_CUSTOM_PARSE_FUNC_PROTOTYPE(ParseConfigDetPgie);

extern "C" bool ParseConfigDetPgie(
    std::vector<NvDsInferLayerInfo> const& outputLayersInfo,
    NvDsInferNetworkInfo const& networkInfo,
    NvDsInferParseDetectionParams const& detectionParams,
    std::vector<NvDsInferObjectDetectionInfo>& objectList)
{
    if (outputLayersInfo.empty()) return false;
    auto const& layer0 = outputLayersInfo[0];

    const unsigned numClasses = detectionParams.numClassesConfigured;
    const float netW = static_cast<float>(networkInfo.width);
    const float netH = static_cast<float>(networkInfo.height);
    const float* data = static_cast<const float*>(layer0.buffer);

    static bool logged = false;
    if (!logged) {
        logged = true;
        fprintf(stderr, "[YOLO11s-det] first call: layer=%s numDims=%d "
                "networkInput=%.0fx%.0f numClasses=%u outputs=%zu\n",
                layer0.layerName ? layer0.layerName : "?",
                layer0.inferDims.numDims, netW, netH, numClasses,
                outputLayersInfo.size());
    }

    // ==== BEGIN GENERATED DECODE ====
    // YOLO11s output shape after batch strip: [84, 8400]
    // layer0.inferDims: numDims=2, d[0]=84, d[1]=8400
    // Each column j (of 8400) is one proposal: rows 0..3 = cx,cy,w,h (in net pixels),
    // rows 4..83 = class scores (post-sigmoid probabilities).
    // Data layout in memory is row-major: data[row * numProposals + col].

    const unsigned int featureDim = layer0.inferDims.d[0]; // 84
    const unsigned int numProposals = layer0.inferDims.d[1]; // 8400
    const unsigned int numCls = (featureDim >= 4u) ? (featureDim - 4u) : 0u;

    if (numCls == 0) return false;

    // Pointers to each row (cx, cy, w, h, then class scores)
    const float* rowCx = data + 0u * numProposals;
    const float* rowCy = data + 1u * numProposals;
    const float* rowW  = data + 2u * numProposals;
    const float* rowH  = data + 3u * numProposals;

    for (unsigned int j = 0; j < numProposals; ++j) {
        // Find best class
        float maxScore = -1.0f;
        unsigned int bestClass = 0;
        for (unsigned int c = 0; c < numCls && c < numClasses; ++c) {
            float s = data[(4u + c) * numProposals + j];
            if (s > maxScore) {
                maxScore = s;
                bestClass = c;
            }
        }

        // Per-class threshold
        float thr = (bestClass < detectionParams.perClassPreclusterThreshold.size())
                     ? detectionParams.perClassPreclusterThreshold[bestClass]
                     : 0.35f;
        if (maxScore < thr) continue;

        // Box in network-input pixel coords (cx, cy, w, h already in pixels)
        float cx = rowCx[j];
        float cy = rowCy[j];
        float bw = rowW[j];
        float bh = rowH[j];

        float left = cx - bw * 0.5f;
        float top  = cy - bh * 0.5f;

        // Clamp to network input
        left = std::max(left, 0.0f);
        top  = std::max(top, 0.0f);
        float right  = std::min(cx + bw * 0.5f, netW);
        float bottom = std::min(cy + bh * 0.5f, netH);

        float finalW = right - left;
        float finalH = bottom - top;
        if (finalW <= 1.0f || finalH <= 1.0f) continue;

        NvDsInferObjectDetectionInfo obj;
        obj.classId = bestClass;
        obj.left = left;
        obj.top = top;
        obj.width = finalW;
        obj.height = finalH;
        obj.detectionConfidence = maxScore;
        objectList.push_back(obj);
    }
    // ==== END GENERATED DECODE ====
    return true;
}