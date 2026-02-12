"""
Smart Recommendation Routes
API endpoints for intelligent, time-aware, view-based recommendations
"""

from fastapi import APIRouter, Depends, Query
from typing import Optional
import logging

from app.firebase.firebase_auth import get_current_user
from app.services.smart_recommendation_service import smart_recommendation_service

router = APIRouter(prefix="/smart", tags=["Smart Recommendations"])
logger = logging.getLogger(__name__)


@router.get("/recommendations")
async def get_smart_recommendations(
    limit: int = Query(30, ge=1, le=100, description="Number of recommendations"),
    quality: str = Query("medium_quality", description="Quality level: high_quality, medium_quality, emerging"),
    current_user: dict = Depends(get_current_user)
):
    """
    Get smart recommendations based on:
    - User mood preferences
    - Current time of day (morning/afternoon/evening/night)
    - Current date and season
    - Trusted YouTube channels
    - View counts (filtered by quality level)
    - User listening history (excludes already played)
    
    Quality levels:
    - high_quality: 1M+ views
    - medium_quality: 100K+ views (default)
    - emerging: 10K+ views
    """
    try:
        uid = current_user.get("uid")
        
        # Validate quality level
        valid_qualities = ['high_quality', 'medium_quality', 'emerging']
        if quality not in valid_qualities:
            quality = 'medium_quality'
        
        logger.info(f"🎯 Smart recommendations request: uid={uid}, limit={limit}, quality={quality}")
        
        recommendations = await smart_recommendation_service.get_smart_recommendations(
            uid=uid,
            limit=limit,
            quality_level=quality
        )
        
        return {
            "success": True,
            "recommendations": recommendations,
            "count": len(recommendations),
            "quality_level": quality,
            "context": smart_recommendation_service._get_current_date_context()
        }
        
    except Exception as e:
        logger.error(f"❌ Smart recommendations error: {e}")
        return {
            "success": False,
            "error": str(e),
            "recommendations": []
        }


@router.get("/feed")
async def get_continuous_feed(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=50, description="Items per page"),
    current_user: dict = Depends(get_current_user)
):
    """
    Get continuous feed of smart recommendations
    Supports pagination for infinite scroll
    
    Perfect for:
    - Home feed
    - Infinite scroll
    - Continuous playback
    """
    try:
        uid = current_user.get("uid")
        
        logger.info(f"📜 Continuous feed request: uid={uid}, page={page}, page_size={page_size}")
        
        feed = await smart_recommendation_service.get_continuous_feed(
            uid=uid,
            page=page,
            page_size=page_size
        )
        
        return {
            "success": True,
            **feed
        }
        
    except Exception as e:
        logger.error(f"❌ Continuous feed error: {e}")
        return {
            "success": False,
            "error": str(e),
            "songs": [],
            "page": page,
            "page_size": page_size,
            "total": 0,
            "has_more": False
        }


@router.get("/time-context")
async def get_time_context(
    current_user: dict = Depends(get_current_user)
):
    """
    Get current time context for recommendations
    Useful for debugging and understanding recommendation logic
    """
    try:
        context = smart_recommendation_service._get_current_date_context()
        time_of_day = context['time_of_day']
        
        # Get appropriate moods for current time
        time_moods = smart_recommendation_service.TIME_MOODS.get(time_of_day, [])
        
        return {
            "success": True,
            "context": context,
            "recommended_moods": time_moods,
            "message": f"It's {time_of_day} on {context['weekday']}, {context['month']} {context['day']}, {context['year']}"
        }
        
    except Exception as e:
        logger.error(f"❌ Time context error: {e}")
        return {
            "success": False,
            "error": str(e)
        }


@router.get("/quality-stats")
async def get_quality_stats(
    current_user: dict = Depends(get_current_user)
):
    """
    Get statistics about quality filtering
    Shows minimum view counts for each quality level
    """
    return {
        "success": True,
        "quality_levels": {
            "high_quality": {
                "min_views": smart_recommendation_service.MIN_VIEWS['high_quality'],
                "description": "Premium content with 1M+ views"
            },
            "medium_quality": {
                "min_views": smart_recommendation_service.MIN_VIEWS['medium_quality'],
                "description": "Popular content with 100K+ views (default)"
            },
            "emerging": {
                "min_views": smart_recommendation_service.MIN_VIEWS['emerging'],
                "description": "Emerging content with 10K+ views"
            }
        },
        "trusted_channels": {
            "global_labels": len(smart_recommendation_service.trusted_channels.GLOBAL_LABELS),
            "indian_labels": len(smart_recommendation_service.trusted_channels.INDIAN_LABELS),
            "east_asian_labels": len(smart_recommendation_service.trusted_channels.EAST_ASIAN_LABELS),
            "regional_labels": len(smart_recommendation_service.trusted_channels.REGIONAL_LABELS),
            "total_trusted": len(smart_recommendation_service.trusted_channels.ALL_TRUSTED)
        }
    }
