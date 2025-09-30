#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from typing import Dict, List, Any
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.core.config import settings
from app.utils.logger import get_logger

logger = get_logger()
router = APIRouter()

# 全局变量存储请求统计和实时请求数据
request_stats = {
    "totalRequests": 0,
    "successfulRequests": 0,
    "failedRequests": 0,
    "lastRequestTime": time.time(),
    "averageResponseTime": 0
}

live_requests = []


def get_index_html() -> str:
    """获取服务首页HTML"""
    return """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Z AI2 API Python - OpenAI兼容API代理</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
            line-height: 1.6;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 40px;
            margin-top: 40px;
        }
        header {
            text-align: center;
            margin-bottom: 40px;
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 2.5rem;
        }
        .subtitle {
            color: #666;
            font-size: 1.2rem;
            margin-bottom: 30px;
        }
        .links {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 40px;
        }
        .link-card {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: 1px solid #e9ecef;
        }
        .link-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .link-card h3 {
            margin-top: 0;
            color: #007bff;
        }
        .link-card p {
            color: #666;
            margin-bottom: 20px;
        }
        .link-card a {
            display: inline-block;
            background-color: #007bff;
            color: white;
            padding: 10px 20px;
            border-radius: 4px;
            text-decoration: none;
            font-weight: bold;
            transition: background-color 0.3s ease;
        }
        .link-card a:hover {
            background-color: #0056b3;
        }
        .features {
            margin-top: 60px;
        }
        .features h2 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }
        .feature-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }
        .feature-item {
            text-align: center;
            padding: 20px;
        }
        .feature-item i {
            font-size: 2rem;
            color: #007bff;
            margin-bottom: 15px;
        }
        .feature-item h3 {
            color: #333;
            margin-bottom: 10px;
        }
        .feature-item p {
            color: #666;
        }
        footer {
            text-align: center;
            margin-top: 60px;
            padding-top: 20px;
            border-top: 1px solid #e9ecef;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>My Z AI2 API Python</h1>
            <div class="subtitle">OpenAI兼容API代理 for Z.ai GLM-4.5</div>
            <p>一个高性能、易于部署的API代理服务，让你能够使用OpenAI兼容的格式访问Z.ai的GLM-4.5模型。</p>
        </header>
        
        <div class="links">
            <div class="link-card">
                <h3>📖 API文档</h3>
                <p>查看完整的API文档，了解如何使用本服务。</p>
                <a href="/docs">查看文档</a>
            </div>
            
            <div class="link-card">
                <h3>📊 API调用看板</h3>
                <p>实时监控API调用情况，查看请求统计和性能指标。</p>
                <a href="/dashboard">查看看板</a>
            </div>
            
            <div class="link-card">
                <h3>🤖 模型列表</h3>
                <p>查看可用的AI模型列表及其详细信息。</p>
                <a href="/models">查看模型</a>
            </div>
        </div>
        
        <div class="features">
            <h2>功能特性</h2>
            <div class="feature-list">
                <div class="feature-item">
                    <div>🔄</div>
                    <h3>OpenAI API兼容</h3>
                    <p>完全兼容OpenAI的API格式，无需修改客户端代码</p>
                </div>
                
                <div class="feature-item">
                    <div>🌊</div>
                    <h3>流式响应支持</h3>
                    <p>支持实时流式输出，提供更好的用户体验</p>
                </div>
                
                <div class="feature-item">
                    <div>🔐</div>
                    <h3>身份验证</h3>
                    <p>支持API密钥验证，确保服务安全</p>
                </div>
                
                <div class="feature-item">
                    <div>🛠️</div>
                    <h3>灵活配置</h3>
                    <p>通过环境变量进行灵活配置</p>
                </div>
                
                <div class="feature-item">
                    <div>📝</div>
                    <h3>思考过程展示</h3>
                    <p>智能处理并展示模型的思考过程</p>
                </div>
                
                <div class="feature-item">
                    <div>📊</div>
                    <h3>实时监控</h3>
                    <p>提供Web仪表板，实时显示API转发情况和统计信息</p>
                </div>
            </div>
        </div>
        
        <footer>
            <p>© 2024 My Z AI2 API Python. Powered by Python & Z.ai GLM-4.5</p>
        </footer>
    </div>
</body>
</html>
"""


def get_dashboard_html() -> str:
    """获取监控面板HTML"""
    return """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API调用看板</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 20px;
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .stats-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background-color: #f8f9fa;
            border-radius: 6px;
            padding: 15px;
            text-align: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #007bff;
        }
        .stat-label {
            font-size: 14px;
            color: #6c757d;
            margin-top: 5px;
        }
        .requests-container {
            margin-top: 30px;
        }
        .requests-table {
            width: 100%;
            border-collapse: collapse;
        }
        .requests-table th, .requests-table td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        .requests-table th {
            background-color: #f8f9fa;
        }
        .status-success {
            color: #28a745;
        }
        .status-error {
            color: #dc3545;
        }
        .refresh-info {
            text-align: center;
            margin-top: 20px;
            color: #6c757d;
            font-size: 14px;
        }
        .pagination-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 20px;
            gap: 10px;
        }
        .pagination-container button {
            padding: 5px 10px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        .pagination-container button:disabled {
            background-color: #cccccc;
            cursor: not-allowed;
        }
        .pagination-container button:hover:not(:disabled) {
            background-color: #0056b3;
        }
        .chart-container {
            margin-top: 30px;
            height: 300px;
            background-color: #f8f9fa;
            border-radius: 6px;
            padding: 15px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>API调用看板</h1>
        
        <div class="stats-container">
            <div class="stat-card">
                <div class="stat-value" id="total-requests">0</div>
                <div class="stat-label">总请求数</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="successful-requests">0</div>
                <div class="stat-label">成功请求</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="failed-requests">0</div>
                <div class="stat-label">失败请求</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="avg-response-time">0s</div>
                <div class="stat-label">平均响应时间</div>
            </div>
        </div>
        
        <div class="chart-container">
            <h2>请求统计图表</h2>
            <canvas id="requestsChart"></canvas>
        </div>
        
        <div class="requests-container">
            <h2>实时请求</h2>
            <table class="requests-table">
                <thead>
                    <tr>
                        <th>时间</th>
                        <th>模型</th>
                        <th>方法</th>
                        <th>状态</th>
                        <th>耗时</th>
                        <th>User Agent</th>
                    </tr>
                </thead>
                <tbody id="requests-tbody">
                    <!-- 请求记录将通过JavaScript动态添加 -->
                </tbody>
            </table>
            <div class="pagination-container">
                <button id="prev-page" disabled>上一页</button>
                <span id="page-info">第 1 页，共 1 页</span>
                <button id="next-page" disabled>下一页</button>
            </div>
        </div>
        
        <div class="refresh-info">
            数据每5秒自动刷新一次
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        // 全局变量
        let allRequests = [];
        let currentPage = 1;
        const itemsPerPage = 10;
        let requestsChart = null;
        
        // 更新统计数据
        function updateStats() {
            fetch('/dashboard/stats')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('total-requests').textContent = data.totalRequests || 0;
                    document.getElementById('successful-requests').textContent = data.successfulRequests || 0;
                    document.getElementById('failed-requests').textContent = data.failedRequests || 0;
                    document.getElementById('avg-response-time').textContent = ((data.averageResponseTime || 0) / 1000).toFixed(2) + 's';
                })
                .catch(error => console.error('Error fetching stats:', error));
        }
        
        // 更新请求列表
        function updateRequests() {
            fetch('/dashboard/requests')
                .then(response => response.json())
                .then(data => {
                    // 检查数据是否为数组
                    if (!Array.isArray(data)) {
                        console.error('返回的数据不是数组:', data);
                        return;
                    }
                    
                    // 保存所有请求数据
                    allRequests = data;
                    
                    // 按时间倒序排列
                    allRequests.sort((a, b) => {
                        const timeA = new Date(a.timestamp);
                        const timeB = new Date(b.timestamp);
                        return timeB - timeA;
                    });
                    
                    // 更新表格
                    updateTable();
                    
                    // 更新图表
                    updateChart();
                    
                    // 更新分页信息
                    updatePagination();
                })
                .catch(error => console.error('Error fetching requests:', error));
        }
        
        // 更新表格显示
        function updateTable() {
            const tbody = document.getElementById('requests-tbody');
            tbody.innerHTML = '';
            
            // 计算当前页的数据范围
            const startIndex = (currentPage - 1) * itemsPerPage;
            const endIndex = startIndex + itemsPerPage;
            const currentRequests = allRequests.slice(startIndex, endIndex);
            
            currentRequests.forEach(request => {
                const row = document.createElement('tr');
                
                // 格式化时间 - 检查时间戳是否有效
                let timeStr = "Invalid Date";
                if (request.timestamp) {
                    try {
                        const time = new Date(request.timestamp);
                        if (!isNaN(time.getTime())) {
                            timeStr = time.toLocaleTimeString();
                        }
                    } catch (e) {
                        console.error("时间格式化错误:", e);
                    }
                }
                
                // 判断模型名称
                let modelName = "GLM-4.5";
                if (request.path && request.path.includes('glm-4.5v')) {
                    modelName = "GLM-4.5V";
                } else if (request.model) {
                    modelName = request.model;
                }
                
                // 状态样式
                const statusClass = request.status >= 200 && request.status < 300 ? 'status-success' : 'status-error';
                const status = request.status || "undefined";
                
                // 截断 User Agent，避免过长
                let userAgent = request.user_agent || "undefined";
                if (userAgent.length > 30) {
                    userAgent = userAgent.substring(0, 30) + "...";
                }
                
                row.innerHTML = "<td>" + timeStr + "</td>" + 
                               "<td>" + modelName + "</td>" + 
                               "<td>" + (request.method || "undefined") + "</td>" + 
                               "<td class='" + statusClass + "'>" + status + "</td>" + 
                               "<td>" + ((request.duration / 1000).toFixed(2) || "undefined") + "s</td>" + 
                               "<td title='" + (request.user_agent || "") + "'>" + userAgent + "</td>";
                
                tbody.appendChild(row);
            });
        }
        
        // 更新分页信息
        function updatePagination() {
            const totalPages = Math.ceil(allRequests.length / itemsPerPage);
            document.getElementById('page-info').textContent = "第 " + currentPage + " 页，共 " + totalPages + " 页";
            
            document.getElementById('prev-page').disabled = currentPage <= 1;
            document.getElementById('next-page').disabled = currentPage >= totalPages;
        }
        
        // 更新图表
        function updateChart() {
            const ctx = document.getElementById('requestsChart').getContext('2d');
            
            // 准备图表数据 - 最近20条请求的响应时间
            const chartData = allRequests.slice(0, 20).reverse();
            const labels = chartData.map(req => {
                const time = new Date(req.timestamp);
                return time.toLocaleTimeString();
            });
            const responseTimes = chartData.map(req => req.duration);
            
            // 如果图表已存在，先销毁
            if (requestsChart) {
                requestsChart.destroy();
            }
            
            // 创建新图表
            requestsChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: '响应时间 (s)',
                        data: responseTimes.map(time => time / 1000),
                        borderColor: '#007bff',
                        backgroundColor: 'rgba(0, 123, 255, 0.1)',
                        tension: 0.1,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: '响应时间 (s)'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: '时间'
                            }
                        }
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: '最近20条请求的响应时间趋势 (s)'
                        }
                    }
                }
            });
        }
        
        // 分页按钮事件
        document.getElementById('prev-page').addEventListener('click', function() {
            if (currentPage > 1) {
                currentPage--;
                updateTable();
                updatePagination();
            }
        });
        
        document.getElementById('next-page').addEventListener('click', function() {
            const totalPages = Math.ceil(allRequests.length / itemsPerPage);
            if (currentPage < totalPages) {
                currentPage++;
                updateTable();
                updatePagination();
            }
        });
        
        // 初始加载
        updateStats();
        updateRequests();
        
        // 定时刷新
        setInterval(updateStats, 5000);
        setInterval(updateRequests, 5000);
    </script>
</body>
</html>
"""


def get_docs_html() -> str:
    """获取API文档HTML"""
    return """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>My Z AI2 API Python 文档</title>
<style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin: 0;
        padding: 20px;
        background-color: #f5f5f5;
        line-height: 1.6;
    }
    .container {
        max-width: 1200px;
        margin: 0 auto;
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        padding: 30px;
    }
    h1 {
        color: #333;
        text-align: center;
        margin-bottom: 30px;
        border-bottom: 2px solid #007bff;
        padding-bottom: 10px;
    }
    h2 {
        color: #007bff;
        margin-top: 30px;
        margin-bottom: 15px;
    }
    h3 {
        color: #333;
        margin-top: 25px;
        margin-bottom: 10px;
    }
    .endpoint {
        background-color: #f8f9fa;
        border-radius: 6px;
        padding: 15px;
        margin-bottom: 20px;
        border-left: 4px solid #007bff;
    }
    .method {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 4px;
        color: white;
        font-weight: bold;
        margin-right: 10px;
        font-size: 14px;
    }
    .get { background-color: #28a745; }
    .post { background-color: #007bff; }
    .path {
        font-family: monospace;
        background-color: #e9ecef;
        padding: 2px 6px;
        border-radius: 3px;
        font-size: 16px;
    }
    .description {
        margin: 15px 0;
    }
    .parameters {
        margin: 15px 0;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0;
    }
    th, td {
        padding: 10px;
        text-align: left;
        border-bottom: 1px solid #ddd;
    }
    th {
        background-color: #f8f9fa;
        font-weight: bold;
    }
    .example {
        background-color: #f8f9fa;
        border-radius: 6px;
        padding: 15px;
        margin: 15px 0;
        font-family: monospace;
        white-space: pre-wrap;
        overflow-x: auto;
    }
    .note {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 10px 15px;
        margin: 15px 0;
        border-radius: 0 4px 4px 0;
    }
    .response {
        background-color: #f8f9fa;
        border-radius: 6px;
        padding: 15px;
        margin: 15px 0;
        font-family: monospace;
        white-space: pre-wrap;
        overflow-x: auto;
    }
    .tab {
        overflow: hidden;
        border: 1px solid #ccc;
        background-color: #f1f1f1;
        border-radius: 4px 4px 0 0;
    }
    .tab button {
        background-color: inherit;
        float: left;
        border: none;
        outline: none;
        cursor: pointer;
        padding: 14px 16px;
        transition: 0.3s;
        font-size: 16px;
    }
    .tab button:hover {
        background-color: #ddd;
    }
    .tab button.active {
        background-color: #ccc;
    }
    .tabcontent {
        display: none;
        padding: 6px 12px;
        border: 1px solid #ccc;
        border-top: none;
        border-radius: 0 0 4px 4px;
    }
    .toc {
        background-color: #f8f9fa;
        border-radius: 6px;
        padding: 15px;
        margin-bottom: 20px;
    }
    .toc ul {
        padding-left: 20px;
    }
    .toc li {
        margin: 5px 0;
    }
    .toc a {
        color: #007bff;
        text-decoration: none;
    }
    .toc a:hover {
        text-decoration: underline;
    }
</style>
</head>
<body>
<div class="container">
    <h1>My Z AI2 API Python 文档</h1>
    
    <div class="toc">
        <h2>目录</h2>
        <ul>
            <li><a href="#overview">概述</a></li>
            <li><a href="#authentication">身份验证</a></li>
            <li><a href="#endpoints">API端点</a>
                <ul>
                    <li><a href="#models">获取模型列表</a></li>
                    <li><a href="#chat-completions">聊天完成</a></li>
                </ul>
            </li>
            <li><a href="#examples">使用示例</a></li>
            <li><a href="#error-handling">错误处理</a></li>
        </ul>
    </div>
    
    <section id="overview">
        <h2>概述</h2>
        <p>这是一个为Z.ai GLM-4.5模型提供OpenAI兼容API接口的代理服务器。它允许你使用标准的OpenAI API格式与Z.ai的GLM-4.5模型进行交互，支持流式和非流式响应。</p>
        <p><strong>基础URL:</strong> <code>http://localhost:7860/v1</code></p>
        <div class="note">
            <strong>注意:</strong> 默认端口为7860，可以通过环境变量PORT进行修改。
        </div>
    </section>
    
    <section id="authentication">
        <h2>身份验证</h2>
        <p>所有API请求都需要在请求头中包含有效的API密钥进行身份验证：</p>
        <div class="example">
Authorization: Bearer your-api-key</div>
        <p>默认的API密钥为 <code>ljq-key</code>，可以通过环境变量 <code>AUTH_TOKEN</code> 进行修改。</p>
    </section>
    
    <section id="endpoints">
        <h2>API端点</h2>
        
        <div class="endpoint" id="models">
    <h3>获取模型列表</h3>
    <div>
        <span class="method get">GET</span>
        <span class="path">/v1/models</span> (JSON数据) 或 <span class="path">/models</span> (HTML页面)
    </div>
            <div class="description">
                <p>获取可用模型列表。可以通过两种方式访问：</p>
                <ul>
                    <li><code>/v1/models</code> - 返回 JSON 格式的模型数据，适用于 API 调用</li>
                    <li><code>/models</code> - 返回美观的 HTML 页面，适用于浏览器查看</li>
                </ul>
            </div>
            <div class="parameters">
                <h4>请求参数</h4>
                <p>无</p>
            </div>
            <div class="response">
{
  "object": "list",
  "data": [
    {
      "id": "GLM-4.5",
      "object": "model",
      "created": 1756788845,
      "owned_by": "z.ai"
    }
  ]
}</div>
        </div>
        
        <div class="endpoint" id="chat-completions">
            <h3>聊天完成</h3>
            <div>
                <span class="method post">POST</span>
                <span class="path">/v1/chat/completions</span>
            </div>
            <div class="description">
                <p>基于消息列表生成模型响应。支持流式和非流式两种模式。</p>
            </div>
            <div class="parameters">
                <h4>请求参数</h4>
                <table>
                    <thead>
                        <tr>
                            <th>参数名</th>
                            <th>类型</th>
                            <th>必需</th>
                            <th>说明</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>model</td>
                            <td>string</td>
                            <td>是</td>
                            <td>要使用的模型ID，例如 "GLM-4.5"</td>
                        </tr>
                        <tr>
                            <td>messages</td>
                            <td>array</td>
                            <td>是</td>
                            <td>消息列表，包含角色和内容</td>
                        </tr>
                        <tr>
                            <td>stream</td>
                            <td>boolean</td>
                            <td>否</td>
                            <td>是否使用流式响应，默认为false</td>
                        </tr>
                        <tr>
                            <td>temperature</td>
                            <td>number</td>
                            <td>否</td>
                            <td>采样温度，控制随机性</td>
                        </tr>
                        <tr>
                            <td>max_tokens</td>
                            <td>integer</td>
                            <td>否</td>
                            <td>生成的最大令牌数</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="parameters">
                <h4>消息格式</h4>
                <table>
                    <thead>
                        <tr>
                            <th>字段</th>
                            <th>类型</th>
                            <th>说明</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>role</td>
                            <td>string</td>
                            <td>消息角色，可选值：system、user、assistant</td>
                        </tr>
                        <tr>
                            <td>content</td>
                            <td>string</td>
                            <td>消息内容</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </section>
    
    <section id="examples">
        <h2>使用示例</h2>
        
        <div class="tab">
            <button class="tablinks active" onclick="openTab(event, 'python-tab')">Python</button>
            <button class="tablinks" onclick="openTab(event, 'curl-tab')">cURL</button>
            <button class="tablinks" onclick="openTab(event, 'javascript-tab')">JavaScript</button>
        </div>
        
        <div id="python-tab" class="tabcontent" style="display: block;">
            <h3>Python示例</h3>
            <div class="example">
import openai

# 配置客户端
client = openai.OpenAI(
    api_key="your-api-key",  # 对应 AUTH_TOKEN
    base_url="http://localhost:7860/v1"
)

# 非流式请求 - 使用GLM-4.5
response = client.chat.completions.create(
    model="GLM-4.5",
    messages=[{"role": "user", "content": "你好，请介绍一下自己"}]
)

print(response.choices[0].message.content)


# 流式请求 - 使用GLM-4.5
response = client.chat.completions.create(
    model="GLM-4.5",
    messages=[{"role": "user", "content": "请写一首关于春天的诗"}],
    stream=True
)


for chunk in response:
if chunk.choices[0].delta.content:
    print(chunk.choices[0].delta.content, end="")</div>
        </div>
        
        <div id="curl-tab" class="tabcontent">
            <h3>cURL示例</h3>
            <div class="example">
# 非流式请求
curl -X POST http://localhost:7860/v1/chat/completions \
-H "Content-Type: application/json" \
-H "Authorization: Bearer your-api-key" \
-d '{
"model": "GLM-4.5",
"messages": [{"role": "user", "content": "你好"}],
"stream": false
}'

# 流式请求
curl -X POST http://localhost:7860/v1/chat/completions \
-H "Content-Type: application/json" \
-H "Authorization: Bearer your-api-key" \
-d '{
"model": "GLM-4.5",
"messages": [{"role": "user", "content": "你好"}],
"stream": true
}'</div>
        </div>
        
        <div id="javascript-tab" class="tabcontent">
            <h3>JavaScript示例</h3>
            <div class="example">
const fetch = require('node-fetch');

async function chatWithGLM(message, stream = false) {
const response = await fetch('http://localhost:7860/v1/chat/completions', {
method: 'POST',
headers: {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer your-api-key'
},
body: JSON.stringify({
  model: 'GLM-4.5',
  messages: [{ role: 'user', content: message }],
  stream: stream
})
});

if (stream) {
// 处理流式响应
const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  
  const chunk = decoder.decode(value);
  const lines = chunk.split('\n');
  
  for (const line of lines) {
    if (line.startsWith('data: ')) {
      const data = line.slice(6);
      if (data === '[DONE]') {
        console.log('\n流式响应完成');
        return;
      }
      
      try {
        const parsed = JSON.parse(data);
        const content = parsed.choices[0]?.delta?.content;
        if (content) {
          process.stdout.write(content);
        }
      } catch (e) {
        // 忽略解析错误
      }
    }
  }
}
} else {
// 处理非流式响应
const data = await response.json();
console.log(data.choices[0].message.content);
}
}

// 使用示例
chatWithGLM('你好，请介绍一下JavaScript', false);</div>
        </div>
    </section>
    
    <section id="error-handling">
        <h2>错误处理</h2>
        <p>API使用标准HTTP状态码来表示请求的成功或失败：</p>
        <table>
            <thead>
                <tr>
                    <th>状态码</th>
                    <th>说明</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>200 OK</td>
                    <td>请求成功</td>
                </tr>
                <tr>
                    <td>400 Bad Request</td>
                    <td>请求格式错误或参数无效</td>
                </tr>
                <tr>
                    <td>401 Unauthorized</td>
                    <td>API密钥无效或缺失</td>
                </tr>
                <tr>
                    <td>502 Bad Gateway</td>
                    <td>上游服务错误</td>
                </tr>
            </tbody>
        </table>
        <div class="note">
            <strong>注意:</strong> 在调试模式下，服务器会输出详细的日志信息，可以通过设置环境变量 DEBUG_LOGGING=true 来启用。
        </div>
    </section>
</div>

<script>
    function openTab(evt, tabName) {
        var i, tabcontent, tablinks;
        tabcontent = document.getElementsByClassName("tabcontent");
        for (i = 0; i < tabcontent.length; i++) {
            tabcontent[i].style.display = "none";
        }
        tablinks = document.getElementsByClassName("tablinks");
        for (i = 0; i < tablinks.length; i++) {
            tablinks[i].className = tablinks[i].className.replace(" active", "");
        }
        document.getElementById(tabName).style.display = "block";
        evt.currentTarget.className += " active";
    }
</script>
</body>
</html>
"""


@router.get("/")
async def index():
    """服务首页"""
    return HTMLResponse(content=get_index_html())


@router.get("/dashboard")
async def dashboard():
    """监控面板"""
    return HTMLResponse(content=get_dashboard_html())


@router.get("/docs")
async def docs():
    """API文档"""
    return HTMLResponse(content=get_docs_html())


@router.get("/dashboard/stats")
async def dashboard_stats():
    """获取统计数据"""
    global request_stats
    return JSONResponse(content=request_stats)


@router.get("/dashboard/requests")
async def dashboard_requests():
    """获取实时请求数据"""
    global live_requests
    return JSONResponse(content=live_requests)


def update_request_stats(path: str, status: int, duration: float):
    """更新请求统计"""
    global request_stats
    request_stats["totalRequests"] += 1
    request_stats["lastRequestTime"] = time.time()
    
    if status >= 200 and status < 300:
        request_stats["successfulRequests"] += 1
    else:
        request_stats["failedRequests"] += 1
    
    # 更新平均响应时间
    if request_stats["totalRequests"] > 0:
        total_duration = request_stats["averageResponseTime"] * (request_stats["totalRequests"] - 1) + duration
        request_stats["averageResponseTime"] = total_duration / request_stats["totalRequests"]


def add_live_request(method: str, path: str, status: int, duration: float, user_agent: str, model: str = None):
    """添加实时请求记录"""
    global live_requests
    
    request = {
        "id": str(int(time.time() * 1000)),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "method": method,
        "path": path,
        "status": status,
        "duration": duration,
        "user_agent": user_agent,
        "model": model or "GLM-4.5"
    }
    
    live_requests.append(request)
    
    # 只保留最近的100条请求
    if len(live_requests) > 100:
        live_requests = live_requests[1:]


def get_models_html() -> str:
    """获取模型列表HTML页面"""
    return """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>模型列表 - My Z AI2 API Python</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            line-height: 1.6;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 30px;
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
        }
        .model-card {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 4px solid #007bff;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .model-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .model-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        .model-name {
            font-size: 1.5rem;
            font-weight: bold;
            color: #333;
            margin: 0;
        }
        .model-id {
            font-family: monospace;
            background-color: #e9ecef;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.9rem;
            color: #495057;
        }
        .model-description {
            color: #666;
            margin-bottom: 15px;
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            margin-bottom: 15px;
        }
        .feature {
            display: flex;
            align-items: center;
            padding: 8px;
            background-color: #e9ecef;
            border-radius: 4px;
            font-size: 0.9rem;
        }
        .feature.supported {
            background-color: #d4edda;
            color: #155724;
        }
        .feature.not-supported {
            background-color: #f8d7da;
            color: #721c24;
        }
        .feature-icon {
            margin-right: 8px;
        }
        .model-details {
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #dee2e6;
        }
        .detail-row {
            display: flex;
            margin-bottom: 8px;
        }
        .detail-label {
            font-weight: bold;
            width: 120px;
            color: #495057;
        }
        .detail-value {
            flex: 1;
        }
        .loading {
            text-align: center;
            padding: 20px;
            color: #6c757d;
        }
        .error {
            text-align: center;
            padding: 20px;
            color: #dc3545;
            background-color: #f8d7da;
            border-radius: 4px;
            margin: 20px 0;
        }
        .refresh-btn {
            display: block;
            margin: 20px auto;
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 1rem;
            transition: background-color 0.3s ease;
        }
        .refresh-btn:hover {
            background-color: #0056b3;
        }
        .back-to-home {
            display: inline-block;
            margin-bottom: 20px;
            color: #007bff;
            text-decoration: none;
        }
        .back-to-home:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>模型列表</h1>
        
        <a href="/" class="back-to-home">← 返回首页</a>
        
        <button class="refresh-btn" onclick="loadModels()">刷新模型列表</button>
        
        <div id="models-container">
            <div class="loading">正在加载模型列表...</div>
        </div>
    </div>

    <script>
        // 加载模型列表
        async function loadModels() {
            const container = document.getElementById('models-container');
            
            try {
                container.innerHTML = '<div class="loading">正在加载模型列表...</div>';
                
                const response = await fetch('/v1/models');
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const data = await response.json();
                
                if (!data.data || !Array.isArray(data.data)) {
                    throw new Error('Invalid data format');
                }
                
                if (data.data.length === 0) {
                    container.innerHTML = '<div class="error">没有找到可用的模型</div>';
                    return;
                }
                
                // 渲染模型列表
                let html = '';
                data.data.forEach(model => {
                    html += createModelCard(model);
                });
                
                container.innerHTML = html;
                
            } catch (error) {
                console.error('Error loading models:', error);
                container.innerHTML = `<div class="error">加载模型列表失败: ${error.message}</div>`;
            }
        }
        
        // 创建模型卡片HTML
        function createModelCard(model) {
            const features = getModelFeatures(model);
            const details = getModelDetails(model);
            
            return `
                <div class="model-card">
                    <div class="model-header">
                        <h2 class="model-name">${model.id || '未知模型'}</h2>
                        <span class="model-id">${model.id || 'N/A'}</span>
                    </div>
                    
                    <div class="model-description">
                        ${getModelDescription(model)}
                    </div>
                    
                    <div class="features">
                        ${features.map(feature => `
                            <div class="feature ${feature.supported ? 'supported' : 'not-supported'}">
                                <span class="feature-icon">${feature.supported ? '✓' : '✗'}</span>
                                ${feature.name}
                            </div>
                        `).join('')}
                    </div>
                    
                    <div class="model-details">
                        ${details.map(detail => `
                            <div class="detail-row">
                                <div class="detail-label">${detail.label}:</div>
                                <div class="detail-value">${detail.value}</div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }
        
        // 获取模型特性
        function getModelFeatures(model) {
            const modelId = (model.id || '').toLowerCase();
            
            // 根据模型ID确定特性
            if (modelId.includes('glm-4.5v') || modelId.includes('vision')) {
                return [
                    { name: '多模态理解', supported: true },
                    { name: '图像识别', supported: true },
                    { name: '视频分析', supported: true },
                    { name: '文档处理', supported: true },
                    { name: '工具调用', supported: false },
                    { name: '思考过程', supported: true }
                ];
            } else if (modelId.includes('glm-4.5') || modelId.includes('gpt-4')) {
                return [
                    { name: '多模态理解', supported: false },
                    { name: '图像识别', supported: false },
                    { name: '视频分析', supported: false },
                    { name: '文档处理', supported: false },
                    { name: '工具调用', supported: true },
                    { name: '思考过程', supported: true }
                ];
            } else {
                // 默认特性
                return [
                    { name: '文本对话', supported: true },
                    { name: '代码生成', supported: true },
                    { name: '逻辑推理', supported: true },
                    { name: '多语言', supported: true }
                ];
            }
        }
        
        // 获取模型描述
        function getModelDescription(model) {
            const modelId = (model.id || '').toLowerCase();
            
            if (modelId.includes('glm-4.5v') || modelId.includes('vision')) {
                return 'GLM-4.5V 是一款支持全方位多模态理解的高级AI模型，能够处理图像、视频、文档等多种媒体类型的内容分析。';
            } else if (modelId.includes('glm-4.5') || modelId.includes('gpt-4')) {
                return 'GLM-4.5 是一款强大的通用对话模型，擅长文本理解、代码生成、逻辑推理和工具调用等任务。';
            } else {
                return '这是一个功能强大的AI模型，支持多种自然语言处理任务。';
            }
        }
        
        // 获取模型详情
        function getModelDetails(model) {
            return [
                { label: '模型ID', value: model.id || 'N/A' },
                { label: '模型类型', value: model.object || 'model' },
                { label: '创建时间', value: model.created ? new Date(model.created * 1000).toLocaleString() : 'N/A' },
                { label: '提供方', value: model.owned_by || 'N/A' }
            ];
        }
        
        // 页面加载时自动加载模型列表
        document.addEventListener('DOMContentLoaded', loadModels);
    </script>
</body>
</html>
"""


@router.get("/models")
async def models_list():
    """模型列表页面"""
    return HTMLResponse(content=get_models_html())