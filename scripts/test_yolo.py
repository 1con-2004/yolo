#!/usr/bin/env python3
"""
YOLOv8基础功能测试脚本
"""

from ultralytics import YOLO
import cv2
import time
import numpy as np

def test_yolo_basic():
    """测试YOLOv8基础功能"""
    print("=== YOLOv8基础功能测试 ===")
    
    try:
        # 加载YOLOv8n模型（会自动下载）
        print("正在加载YOLOv8n模型...")
        model = YOLO('yolov8n.pt')
        print("✅ YOLOv8n模型加载成功")
        
        # 创建一个测试图片（包含人物的样例）
        print("创建测试图片...")
        
        # 使用OpenCV创建一个简单的测试图像
        test_img = np.zeros((640, 640, 3), dtype=np.uint8)
        # 添加一些简单的形状作为测试
        cv2.rectangle(test_img, (100, 100), (300, 500), (255, 255, 255), -1)
        cv2.circle(test_img, (200, 200), 50, (0, 255, 0), -1)
        
        # 保存测试图片
        cv2.imwrite('test_images/sample.jpg', test_img)
        print("✅ 测试图片创建完成")
        
        # 进行预测
        print("开始进行目标检测...")
        start_time = time.time()
        results = model('test_images/sample.jpg')
        end_time = time.time()
        
        print(f"✅ 检测完成，耗时: {(end_time - start_time)*1000:.2f}ms")
        
        # 分析结果
        for i, result in enumerate(results):
            print(f"\n--- 结果 {i+1} ---")
            print(f"检测到的对象数量: {len(result.boxes) if result.boxes else 0}")
            
            if result.boxes:
                for j, box in enumerate(result.boxes):
                    conf = box.conf.cpu().numpy()[0]
                    cls = int(box.cls.cpu().numpy()[0])
                    class_name = model.names[cls]
                    print(f"  对象 {j+1}: {class_name} (置信度: {conf:.3f})")
            
            # 输出张量形状信息
            if hasattr(result, 'orig_shape'):
                print(f"原始图像尺寸: {result.orig_shape}")
            
        # 保存检测结果
        results[0].save('test_images/result.jpg')
        print("✅ 检测结果已保存到 test_images/result.jpg")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def analyze_output_format():
    """分析YOLOv8输出格式"""
    print("\n=== YOLOv8输出格式分析 ===")
    
    try:
        model = YOLO('yolov8n.pt')
        results = model('test_images/sample.jpg')
        
        for result in results:
            print(f"结果类型: {type(result)}")
            
            if result.boxes:
                boxes = result.boxes
                print(f"检测框数量: {len(boxes)}")
                print(f"boxes类型: {type(boxes)}")
                print(f"boxes.data形状: {boxes.data.shape}")
                print(f"boxes.xyxy形状: {boxes.xyxy.shape}")
                print(f"boxes.conf形状: {boxes.conf.shape}")
                print(f"boxes.cls形状: {boxes.cls.shape}")
                
                # 打印第一个检测框的详细信息
                if len(boxes) > 0:
                    print(f"\n第一个检测框详情:")
                    print(f"  坐标 (xyxy): {boxes.xyxy[0].cpu().numpy()}")
                    print(f"  置信度: {boxes.conf[0].cpu().numpy()}")
                    print(f"  类别ID: {boxes.cls[0].cpu().numpy()}")
                    print(f"  类别名称: {model.names[int(boxes.cls[0])]}")
        
        return True
        
    except Exception as e:
        print(f"❌ 输出格式分析失败: {e}")
        return False

def test_model_sizes():
    """测试不同大小的模型"""
    print("\n=== 测试不同模型大小 ===")
    
    models = ['yolov8n.pt', 'yolov8s.pt', 'yolov8m.pt']
    results = {}
    
    for model_name in models:
        print(f"\n测试 {model_name}...")
        try:
            model = YOLO(model_name)
            
            # 进行5次测试取平均值
            times = []
            for i in range(5):
                start_time = time.time()
                result = model('test_images/sample.jpg')
                end_time = time.time()
                times.append((end_time - start_time) * 1000)
            
            avg_time = np.mean(times)
            std_time = np.std(times)
            
            results[model_name] = {
                'avg_time': avg_time,
                'std_time': std_time,
                'detections': len(result[0].boxes) if result[0].boxes else 0
            }
            
            print(f"  平均推理时间: {avg_time:.2f}ms ± {std_time:.2f}ms")
            print(f"  检测对象数量: {results[model_name]['detections']}")
            
        except Exception as e:
            print(f"  ❌ {model_name} 测试失败: {e}")
            results[model_name] = None
    
    # 打印性能对比
    print("\n=== 性能对比总结 ===")
    for model_name, result in results.items():
        if result:
            print(f"{model_name:12}: {result['avg_time']:6.2f}ms, "
                  f"检测数量: {result['detections']}")
    
    return results

if __name__ == "__main__":
    print("开始YOLOv8测试...")
    
    # 基础功能测试
    if test_yolo_basic():
        print("✅ 基础功能测试通过")
        
        # 输出格式分析
        if analyze_output_format():
            print("✅ 输出格式分析完成")
            
            # 模型大小测试
            model_results = test_model_sizes()
            print("✅ 模型性能测试完成")
            
            print("\n🎉 所有测试完成！")
        else:
            print("❌ 输出格式分析失败")
    else:
        print("❌ 基础功能测试失败")