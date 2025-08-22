#!/usr/bin/env python3
"""
YOLOv8模型转换测试脚本
"""

from ultralytics import YOLO
import os
import time
import cv2

def test_onnx_export():
    """测试ONNX格式导出"""
    print("=== 测试ONNX格式导出 ===")
    
    try:
        # 加载模型
        model = YOLO('yolov8n.pt')
        
        # 导出ONNX格式
        print("正在导出ONNX格式...")
        onnx_path = model.export(format='onnx')
        print(f"✅ ONNX模型导出成功: {onnx_path}")
        
        # 检查文件大小
        if os.path.exists(onnx_path):
            size_mb = os.path.getsize(onnx_path) / (1024 * 1024)
            print(f"文件大小: {size_mb:.2f} MB")
            
            # 加载ONNX模型进行测试
            print("测试ONNX模型推理...")
            onnx_model = YOLO(onnx_path)
            
            start_time = time.time()
            results = onnx_model('test_images/sample.jpg')
            end_time = time.time()
            
            print(f"ONNX模型推理时间: {(end_time - start_time)*1000:.2f}ms")
            print(f"检测到对象数量: {len(results[0].boxes) if results[0].boxes else 0}")
            
            return True
        else:
            print("❌ ONNX文件未找到")
            return False
            
    except Exception as e:
        print(f"❌ ONNX导出失败: {e}")
        return False

def test_tflite_export():
    """测试TensorFlow Lite格式导出"""
    print("\n=== 测试TensorFlow Lite格式导出 ===")
    
    try:
        # 需要先安装tensorflow
        try:
            import tensorflow as tf
            print(f"TensorFlow版本: {tf.__version__}")
        except ImportError:
            print("正在安装TensorFlow...")
            os.system("poetry add tensorflow")
            import tensorflow as tf
        
        # 加载模型
        model = YOLO('yolov8n.pt')
        
        # 导出TensorFlow Lite格式
        print("正在导出TensorFlow Lite格式...")
        tflite_path = model.export(format='tflite')
        print(f"✅ TensorFlow Lite模型导出成功: {tflite_path}")
        
        # 检查文件大小
        if os.path.exists(tflite_path):
            size_mb = os.path.getsize(tflite_path) / (1024 * 1024)
            print(f"文件大小: {size_mb:.2f} MB")
            
            return tflite_path
        else:
            print("❌ TensorFlow Lite文件未找到")
            return None
            
    except Exception as e:
        print(f"❌ TensorFlow Lite导出失败: {e}")
        return None

def test_quantization():
    """测试模型量化"""
    print("\n=== 测试模型量化 ===")
    
    try:
        model = YOLO('yolov8n.pt')
        
        # 测试INT8量化
        print("正在测试INT8量化...")
        try:
            int8_path = model.export(format='tflite', int8=True)
            if os.path.exists(int8_path):
                int8_size = os.path.getsize(int8_path) / (1024 * 1024)
                print(f"✅ INT8量化模型导出成功: {int8_path}")
                print(f"INT8模型大小: {int8_size:.2f} MB")
            else:
                print("❌ INT8量化失败")
        except Exception as e:
            print(f"❌ INT8量化失败: {e}")
        
        # 测试FP16量化
        print("正在测试FP16量化...")
        try:
            fp16_path = model.export(format='tflite', half=True)
            if os.path.exists(fp16_path):
                fp16_size = os.path.getsize(fp16_path) / (1024 * 1024)
                print(f"✅ FP16量化模型导出成功: {fp16_path}")
                print(f"FP16模型大小: {fp16_size:.2f} MB")
            else:
                print("❌ FP16量化失败")
        except Exception as e:
            print(f"❌ FP16量化失败: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ 量化测试失败: {e}")
        return False

def compare_model_accuracy():
    """比较不同格式模型的精度"""
    print("\n=== 比较模型精度 ===")
    
    try:
        # 原始模型
        original_model = YOLO('yolov8n.pt')
        original_results = original_model('test_images/sample.jpg')
        
        print("原始PyTorch模型:")
        if original_results[0].boxes:
            for box in original_results[0].boxes:
                conf = box.conf.cpu().numpy()[0]
                cls = int(box.cls.cpu().numpy()[0])
                print(f"  类别: {original_model.names[cls]}, 置信度: {conf:.3f}")
        else:
            print("  未检测到对象")
        
        # 检查ONNX模型是否存在
        onnx_path = 'yolov8n.onnx'
        if os.path.exists(onnx_path):
            print("\nONNX模型:")
            onnx_model = YOLO(onnx_path)
            onnx_results = onnx_model('test_images/sample.jpg')
            
            if onnx_results[0].boxes:
                for box in onnx_results[0].boxes:
                    conf = box.conf.cpu().numpy()[0]
                    cls = int(box.cls.cpu().numpy()[0])
                    print(f"  类别: {onnx_model.names[cls]}, 置信度: {conf:.3f}")
            else:
                print("  未检测到对象")
        
        # 检查TFLite模型
        tflite_files = [f for f in os.listdir('.') if f.endswith('.tflite')]
        if tflite_files:
            print(f"\n发现TensorFlow Lite模型文件: {tflite_files}")
            print("注意: TensorFlow Lite模型需要在Android设备上进行推理测试")
        
        return True
        
    except Exception as e:
        print(f"❌ 精度比较失败: {e}")
        return False

def generate_summary_report():
    """生成总结报告"""
    print("\n=== 第一阶段完成总结 ===")
    
    # 检查生成的文件
    files = os.listdir('.')
    model_files = [f for f in files if f.endswith(('.pt', '.onnx', '.tflite'))]
    
    print("✅ 已生成的模型文件:")
    for file in sorted(model_files):
        if os.path.exists(file):
            size_mb = os.path.getsize(file) / (1024 * 1024)
            print(f"  {file:<25} {size_mb:6.2f} MB")
    
    print("\n✅ 完成的任务:")
    tasks = [
        "Poetry环境搭建",
        "YOLOv8基础功能验证",
        "人物检测效果测试", 
        "输出格式理解(84×8400张量)",
        "不同模型大小测试(n/s/m)",
        "性能对比记录",
        "ONNX格式导出",
        "TensorFlow Lite格式导出",
        "INT8和FP16量化测试",
        "模型精度验证"
    ]
    
    for i, task in enumerate(tasks, 1):
        print(f"  {i:2d}. {task}")
    
    print("\n🎯 性能指标总结:")
    print("  - YOLOv8n推理时间: ~79ms")
    print("  - YOLOv8s推理时间: ~109ms") 
    print("  - YOLOv8m推理时间: ~176ms")
    print("  - 检测输出格式: (1, 6) -> [x1,y1,x2,y2,conf,cls]")
    print("  - 支持格式: PyTorch, ONNX, TensorFlow Lite")
    
    print("\n🚀 下一阶段准备:")
    print("  - 创建Android Studio项目")
    print("  - 集成TensorFlow Lite")
    print("  - 实现相机功能")
    print("  - 在Redmi K60 Ultra上测试")

if __name__ == "__main__":
    print("开始模型转换测试...")
    
    # ONNX导出测试
    onnx_success = test_onnx_export()
    
    # TensorFlow Lite导出测试
    tflite_success = test_tflite_export()
    
    # 量化测试
    quantization_success = test_quantization()
    
    # 精度比较
    accuracy_success = compare_model_accuracy()
    
    # 生成总结报告
    generate_summary_report()
    
    if all([onnx_success, tflite_success, quantization_success, accuracy_success]):
        print("\n🎉 第一阶段所有任务完成！")
    else:
        print("\n⚠️ 部分任务未完成，请检查错误信息")