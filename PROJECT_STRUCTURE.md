# 🏗️ 项目结构说明

基于"站在巨人肩膀上"的开发策略，本项目采用**双轨并行**的架构设计：
- **Python模型工厂**：负责模型优化、转换和验证
- **Android应用**：基于开源项目快速构建用户界面

## 📁 目录结构

```
aimbot/                           # 项目根目录
├── README.md                     # 项目主说明文档
├── environment.yml               # Conda环境配置
├── PROJECT_STRUCTURE.md          # 本文件 - 项目结构说明
│
├── models/                       # 🧠 模型工厂目录
│   ├── yolov8n.pt               # YOLOv8 Nano模型
│   ├── yolov8s.pt               # YOLOv8 Small模型
│   ├── yolov8m.pt               # YOLOv8 Medium模型
│   └── exports/                 # 导出的模型文件
│       ├── yolov8n.tflite      # TensorFlow Lite格式
│       ├── yolov8n.onnx        # ONNX格式
│       └── quantized/          # 量化模型
│
├── scripts/                     # 🔧 Python工具脚本
│   ├── test_yolo.py            # 基础功能测试
│   ├── test_export.py          # 模型转换测试
│   ├── model_converter.py      # 模型格式转换工具
│   └── performance_benchmark.py # 性能基准测试
│
├── android-app/                 # 📱 Android应用目录
│   ├── reference-yolo/         # 参考项目(surendramaran/YOLO)
│   ├── k60-yolo-detector/      # 定制化K60 Ultra应用
│   └── shared-resources/       # 共享资源(模型、图标等)
│
├── docs/                        # 📚 项目文档
│   ├── ARCHITECTURE.md         # 架构设计文档
│   ├── PERFORMANCE.md          # 性能测试报告
│   ├── DEPLOYMENT.md           # 部署指南
│   └── TROUBLESHOOTING.md      # 问题排查手册
│
├── test_images/                 # 🖼️ 测试图片
│   ├── sample.jpg              # 原始测试图片
│   ├── result.jpg              # 检测结果图片
│   └── benchmarks/             # 基准测试图片集
│
├── runs/                        # 🏃 YOLO运行输出
│   └── detect/predict/         # 检测结果缓存
│
└── reference-docs/              # 📖 参考文档和指南
    ├── 快速开始指南.md
    ├── 项目开发任务清单.md
    └── YOLO移动端学习项目.md
```

## 🚀 开发工作流

### Phase 1: Python模型优化 (当前阶段)
```bash
conda activate yolo-mobile
cd scripts/
python model_converter.py        # 模型转换
python performance_benchmark.py  # 性能测试
```

### Phase 2: Android应用集成
```bash
cd android-app/
git clone https://github.com/surendramaran/YOLO.git reference-yolo
# 基于参考项目创建定制版本
```

### Phase 3: 整合优化
```bash
# 将Python生成的.tflite模型集成到Android应用
cp models/exports/yolov8n.tflite android-app/k60-yolo-detector/app/src/main/assets/
```

## 🎯 核心优势

1. **模块化设计** - Python和Android代码完全分离
2. **版本控制** - 不同格式模型统一管理  
3. **快速迭代** - 基于成熟开源项目加速开发
4. **性能优化** - 专门针对K60 Ultra设备特化

## 🔄 文件流转关系

```
[Python环境] → .tflite文件 → [Android应用] → [K60 Ultra设备]
     ↓              ↓              ↓              ↓
  模型训练/优化   格式转换      应用集成       实际部署
```

这种结构设计确保了开发效率的最大化，同时保持了技术栈的专业分工。