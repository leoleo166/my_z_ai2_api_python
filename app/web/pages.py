#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Web页面处理模块
提供服务首页、监控面板、API文档等页面的路由和内容
"""

import time
from typing import Dict, List, Any, Optional
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.config import settings
from app.utils.logger import get_logger
from app.providers import get_provider_router

logger = get_logger()
router = APIRouter()
templates = Jinja2Templates(directory="app/web/templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """服务首页"""
    try:
        # 获取提供商路由器实例
        provider_router = get_provider_router()
        models_list = provider_router.get_models_list()
        
        # 统计模型数量
        models_count = len(models_list.get("data", []))
        
        # 获取提供商列表
        providers = provider_router.factory.list_providers()
        providers_count = len(providers)
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "models_count": models_count,
            "providers_count": providers_count,
            "service_name": settings.SERVICE_NAME,
            "version": "1.0.0"
        })
    except Exception as e:
        logger.error(f"❌ 渲染首页失败: {e}")
        return HTMLResponse(content="<h1>服务暂时不可用</h1><p>请稍后再试</p>", status_code=500)


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """监控面板"""
    try:
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "service_name": settings.SERVICE_NAME
        })
    except Exception as e:
        logger.error(f"❌ 渲染监控面板失败: {e}")
        return HTMLResponse(content="<h1>监控面板暂时不可用</h1><p>请稍后再试</p>", status_code=500)


@router.get("/docs", response_class=HTMLResponse)
async def docs(request: Request):
    """API文档"""
    try:
        # 获取提供商路由器实例
        provider_router = get_provider_router()
        models_list = provider_router.get_models_list()
        
        # 获取所有模型
        models = models_list.get("data", [])
        
        # 按提供商分组模型
        models_by_provider = {}
        for model in models:
            provider = model.get("owned_by", "unknown")
            if provider not in models_by_provider:
                models_by_provider[provider] = []
            models_by_provider[provider].append(model)
        
        return templates.TemplateResponse("docs.html", {
            "request": request,
            "models_by_provider": models_by_provider,
            "service_name": settings.SERVICE_NAME,
            "auth_token": settings.AUTH_TOKEN,
            "listen_port": settings.LISTEN_PORT
        })
    except Exception as e:
        logger.error(f"❌ 渲染API文档失败: {e}")
        return HTMLResponse(content="<h1>API文档暂时不可用</h1><p>请稍后再试</p>", status_code=500)


@router.get("/dashboard/stats")
async def dashboard_stats():
    """获取监控面板统计数据"""
    try:
        # 这里可以添加实际的统计逻辑
        # 目前返回模拟数据
        return {
            "totalRequests": 0,
            "successfulRequests": 0,
            "failedRequests": 0,
            "averageResponseTime": 0
        }
    except Exception as e:
        logger.error(f"❌ 获取统计数据失败: {e}")
        return {
            "totalRequests": 0,
            "successfulRequests": 0,
            "failedRequests": 0,
            "averageResponseTime": 0
        }


@router.get("/dashboard/requests")
async def dashboard_requests():
    """获取实时请求数据"""
    try:
        # 这里可以添加实际的请求记录逻辑
        # 目前返回空数组
        return []
    except Exception as e:
        logger.error(f"❌ 获取请求数据失败: {e}")
        return []