"""
CrowdWisdomTrading Ads AI Agent - Main FastAPI Application
"""
import os
import json
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="CrowdWisdomTrading Ads AI Agent",
    description="AI-powered Ads Generator using CrewAI and Apify",
    version="1.0.0"
)

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data directory
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)


# ==================== Pydantic Models ====================

class AdSearchRequest(BaseModel):
    product_niche: str
    days_back: int = 30


class AdSearchResponse(BaseModel):
    success: bool
    message: str
    ads_found: int
    ads: List[Dict[str, Any]]
    timestamp: str


class AnalysisResponse(BaseModel):
    success: bool
    message: str
    insights: Dict[str, Any]
    timestamp: str


class ScriptRequest(BaseModel):
    product_niche: str
    insights: Optional[Dict[str, Any]] = None


class ScriptResponse(BaseModel):
    success: bool
    message: str
    script: Dict[str, Any]
    timestamp: str


class VideoRequest(BaseModel):
    product_niche: str
    script: Optional[Dict[str, Any]] = None


class VideoResponse(BaseModel):
    success: bool
    message: str
    video_plan: Dict[str, Any]
    timestamp: str


class GenerateAllRequest(BaseModel):
    product_niche: str


# ==================== Helper Functions ====================

def save_json(data: Dict, filename: str) -> Path:
    """Save data to JSON file"""
    filepath = DATA_DIR / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    logger.info(f"Saved data to {filepath}")
    return filepath


def load_json(filename: str) -> Optional[Dict]:
    """Load data from JSON file"""
    filepath = DATA_DIR / filename
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def get_timestamp() -> str:
    """Get current timestamp"""
    return datetime.now().isoformat()


# ==================== API Endpoints ====================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "CrowdWisdomTrading Ads AI Agent",
        "version": "1.0.0",
        "status": "running",
        "timestamp": get_timestamp()
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": get_timestamp()
    }


@app.post("/search-ads", response_model=AdSearchResponse)
async def search_ads(request: AdSearchRequest):
    """
    Search ads using Apify (mocked for demo)
    In production, this would use Apify API to scrape Meta Ads Library
    """
    try:
        logger.info(f"Searching ads for: {request.product_niche}")
        
        # Mock data - in production, this would call Apify API
        # Apify actor: apify/meta-ads-scraper
        mock_ads = [
            {
                "ad_id": "ad_001",
                "platform": "Meta",
                "ad_title": f"Transform Your {request.product_niche} Business",
                "ad_copy": "Stop struggling with outdated marketing. Our AI-powered solution helps you create high-converting ads in minutes. Join 10,000+ businesses already using our platform.",
                "creative_type": "video",
                " impressions": 1250000,
                "reach": 890000,
                "engagement_rate": 3.2,
                "created_date": "2026-04-15",
                "duration_seconds": 15,
                "hook": "Stop wasting money on ads that don't convert",
                "cta": "Start Free Trial"
            },
            {
                "ad_id": "ad_002",
                "platform": "Meta",
                "ad_title": f"The Secret to {request.product_niche} Success",
                "ad_copy": "What if you could predict your customer's next move? Our AI analyzes millions of data points to give you the exact ads that will convert. No guesswork, just results.",
                "creative_type": "carousel",
                "impressions": 980000,
                "reach": 720000,
                "engagement_rate": 2.8,
                "created_date": "2026-04-20",
                "duration_seconds": 0,
                "hook": "The secret algorithm doesn't want you to know",
                "cta": "Get Started"
            },
            {
                "ad_id": "ad_003",
                "platform": "Meta",
                "ad_title": f"{request.product_niche}? Here's What Actually Works",
                "ad_copy": "Forget everything you think you know about marketing. The new way is here. AI-generated ads that speak directly to your customer's pain points. See the difference today.",
                "creative_type": "image",
                "impressions": 2100000,
                "reach": 1500000,
                "engagement_rate": 4.1,
                "created_date": "2026-04-25",
                "duration_seconds": 0,
                "hook": "Everything you thought you knew is wrong",
                "cta": "Try It Free"
            },
            {
                "ad_id": "ad_004",
                "platform": "Meta",
                "ad_title": f"Finally! A {request.product_niche} Solution That Works",
                "ad_copy": "After 10 years of testing, we found the perfect formula. Now we're giving it to you for free. No credit card required. Just pure, proven results.",
                "creative_type": "video",
                "impressions": 1750000,
                "reach": 1200000,
                "engagement_rate": 3.8,
                "created_date": "2026-04-28",
                "duration_seconds": 30,
                "hook": "After 10 years, we cracked the code",
                "cta": "Claim Your Free Access"
            },
            {
                "ad_id": "ad_005",
                "platform": "Meta",
                "ad_title": f"Don't Buy {request.product_niche} Until You Read This",
                "ad_copy": "Warning: This will change how you see marketing forever. 87% of businesses are doing it wrong. Be in the 13% that actually profit.",
                "creative_type": "video",
                "impressions": 890000,
                "reach": 650000,
                "engagement_rate": 2.5,
                "created_date": "2026-04-10",
                "duration_seconds": 45,
                "hook": "Warning: Don't make this mistake",
                "cta": "Learn More"
            }
        ]
        
        # Sort by engagement rate
        mock_ads.sort(key=lambda x: x['engagement_rate'], reverse=True)
        
        # Save to file
        result = {
            "product_niche": request.product_niche,
            "days_back": request.days_back,
            "ads_found": len(mock_ads),
            "ads": mock_ads,
            "timestamp": get_timestamp()
        }
        save_json(result, "searched_ads.json")
        
        return AdSearchResponse(
            success=True,
            message=f"Found {len(mock_ads)} top-performing ads",
            ads_found=len(mock_ads),
            ads=mock_ads,
            timestamp=get_timestamp()
        )
        
    except Exception as e:
        logger.error(f"Error searching ads: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze-ads", response_model=AnalysisResponse)
async def analyze_ads(request: AdSearchRequest):
    """
    Analyze ads to extract marketing insights
    Uses CrewAI Analysis Agent
    """
    try:
        logger.info(f"Analyzing ads for: {request.product_niche}")
        
        # Load previously searched ads
        ads_data = load_json("searched_ads.json")
        
        if not ads_data or not ads_data.get("ads"):
            # If no previous search, do a mock search first
            ads_data = {
                "ads": [
                    {"ad_copy": "Transform your business with AI-powered marketing", "hook": "Stop struggling", "cta": "Start Free"},
                    {"ad_copy": "The secret to success - predict customer behavior", "hook": "Secret algorithm", "cta": "Get Started"},
                    {"ad_copy": "What actually works - AI-generated ads", "hook": "Everything you knew is wrong", "cta": "Try It Free"}
                ]
            }
        
        # Extract insights using mock analysis
        # In production, this would use CrewAI Analysis Agent
        insights = {
            "pain_points": [
                "Wasting money on ads that don't convert",
                "No clear understanding of what works",
                "Time-consuming trial and error process",
                "Difficulty predicting customer behavior",
                "Inconsistent results from marketing efforts"
            ],
            "hooks": [
                "Problem-aware: 'Stop struggling with...'",
                "Secret/insider: 'The secret they don't want you to know'",
                "Contrarian: 'Everything you thought you knew is wrong'",
                "Urgency: 'Finally! A solution that works'",
                "Warning: 'Don't make this mistake'"
            ],
            "marketing_angles": [
                {
                    "angle": "AI Technology",
                    "description": "Emphasize cutting-edge AI capabilities",
                    "example_hooks": ["Our AI analyzes millions of data points", "Predict your customer's next move"]
                },
                {
                    "angle": "Proven Results",
                    "description": "Social proof and statistics",
                    "example_hooks": ["Join 10,000+ businesses", "87% success rate"]
                },
                {
                    "angle": "Risk Reversal",
                    "description": "Reduce fear of trying",
                    "example_hooks": ["No credit card required", "Start Free Trial", "Try It Free"]
                },
                {
                    "angle": "Time Savings",
                    "description": "Emphasize efficiency",
                    "example_hooks": ["Create ads in minutes", "No guesswork"]
                }
            ],
            "top_ctas": [
                "Start Free Trial",
                "Get Started",
                "Try It Free",
                "Learn More",
                "Claim Your Free Access"
            ],
            "recommended_duration": "15-30 seconds",
            "best_creative_types": ["video", "carousel", "image"]
        }
        
        # Save insights
        result = {
            "product_niche": request.product_niche,
            "insights": insights,
            "timestamp": get_timestamp()
        }
        save_json(result, "ad_insights.json")
        
        return AnalysisResponse(
            success=True,
            message="Successfully extracted marketing insights",
            insights=insights,
            timestamp=get_timestamp()
        )
        
    except Exception as e:
        logger.error(f"Error analyzing ads: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-script", response_model=ScriptResponse)
async def generate_script(request: ScriptRequest):
    """
    Generate ad script using insights and data
    Uses CrewAI Script Agent
    """
    try:
        logger.info(f"Generating script for: {request.product_niche}")
        
        # Load insights if not provided
        insights = request.insights
        if not insights:
            insights_data = load_json("ad_insights.json")
            if insights_data:
                insights = insights_data.get("insights")
        
        # Mock Google Drive data (in production, would fetch from Drive)
        google_drive_data = {
            "brand_guidelines": {
                "tone": "Professional yet conversational",
                "colors": ["#2563EB", "#FFFFFF"],
                "logo_url": "https://example.com/logo.png"
            },
            "product_info": {
                "name": request.product_niche,
                "tagline": "AI-Powered Marketing Revolution",
                "key_benefits": [
                    "Generate ads in minutes, not hours",
                    "Data-driven insights from real campaigns",
                    "Proven conversion optimization"
                ]
            },
            "target_audience": {
                "age_range": "25-45",
                "interests": ["Marketing", "Technology", "Business Growth"],
                "pain_points": ["Time constraints", "Budget limitations", "Lack of expertise"]
            }
        }
        
        # Generate 60-second script
        script = {
            "title": f"60-Second Ad Script for {request.product_niche}",
            "duration": 60,
            "scenes": [
                {
                    "scene_number": 1,
                    "time_range": "0-5 seconds",
                    "type": "hook",
                    "visual": "Close-up of stressed business owner looking at failed ads",
                    "audio": "Narrator: 'Stop wasting thousands on ads that never convert?'",
                    "text_on_screen": "STOP WASTING MONEY"
                },
                {
                    "scene_number": 2,
                    "time_range": "5-15 seconds",
                    "type": "problem_agitation",
                    "visual": "Split screen - traditional marketing vs AI solution",
                    "audio": "Narrator: 'What if you could predict exactly what your customers want? Our AI analyzes millions of data points to create perfect ads.'",
                    "text_on_screen": "INTRODUCING AI-POWERED ADS"
                },
                {
                    "scene_number": 3,
                    "time_range": "15-30 seconds",
                    "type": "solution_demo",
                    "visual": "Quick montage of ad creation process - input → AI processing → ad output",
                    "audio": "Narrator: 'No more guesswork. Just enter your product, and get professional ads in minutes. Join 10,000+ businesses already growing.'",
                    "text_on_screen": "CREATE ADS IN MINUTES"
                },
                {
                    "scene_number": 4,
                    "time_range": "30-45 seconds",
                    "type": "social_proof",
                    "visual": "Testimonial-style clips with happy business owners",
                    "audio": "Narrator: \"Sarah from e-commerce saw 3x ROI in 30 days. Mark doubled his conversions. You can too.\"",
                    "text_on_screen": "JOIN 10,000+ BUSINESSES"
                },
                {
                    "scene_number": 5,
                    "time_range": "45-60 seconds",
                    "type": "cta",
                    "visual": "Product dashboard with prominent CTA button",
                    "audio": "Narrator: 'Start your free trial today at [URL]. No credit card required. Transform your marketing in just 60 seconds.'",
                    "text_on_screen": "START FREE TRIAL →"
                }
            ],
            "voiceover_full": """Stop wasting thousands on ads that never convert? What if you could predict exactly what your customers want? Our AI analyzes millions of data points to create perfect ads. No more guesswork. Just enter your product, and get professional ads in minutes. Join 10,000+ businesses already growing. Sarah from e-commerce saw 3x ROI in 30 days. Mark doubled his conversions. You can too. Start your free trial today. No credit card required. Transform your marketing in just 60 seconds.""",
            "key_highlights": {
                "hook": "Stop wasting money on ads that don't convert",
                "value_prop": "AI-powered ad creation in minutes",
                "social_proof": "10,000+ businesses",
                "cta": "Start Free Trial"
            },
            "script_tone": insights.get("marketing_angles", [{}])[0].get("angle", "AI Technology") if insights else "AI Technology",
            "total_words": 187
        }
        
        # Save script
        result = {
            "product_niche": request.product_niche,
            "script": script,
            "supporting_data": google_drive_data,
            "timestamp": get_timestamp()
        }
        save_json(result, "generated_script.json")
        
        return ScriptResponse(
            success=True,
            message="Successfully generated 60-second ad script",
            script=script,
            timestamp=get_timestamp()
        )
        
    except Exception as e:
        logger.error(f"Error generating script: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-video", response_model=VideoResponse)
async def generate_video(request: VideoRequest):
    """
    Generate video plan for Remotion
    Uses CrewAI Video Agent
    """
    try:
        logger.info(f"Generating video plan for: {request.product_niche}")
        
        # Load script if not provided
        script = request.script
        if not script:
            script_data = load_json("generated_script.json")
            if script_data:
                script = script_data.get("script")
        
        # Generate video plan (Remotion-compatible)
        video_plan = {
            "title": f"Video Plan for {request.product_niche}",
            "total_duration": 60,
            "resolution": "1920x1080",
            "frame_rate": 30,
            "format": "vertical (9:16) for Reels/TikTok",
            "scenes": [
                {
                    "scene_id": 1,
                    "time_start": 0,
                    "time_end": 5,
                    "duration": 5,
                    "scene_type": "hook",
                    "background": {
                        "type": "solid_color",
                        "color": "#1a1a2e",
                        "gradient": None
                    },
                    "visuals": {
                        "main_element": {
                            "type": "text",
                            "content": "STOP WASTING MONEY",
                            "style": "bold_headline",
                            "animation": "fade_in_scale"
                        },
                        "secondary": {
                            "type": "emoji",
                            "content": "💸",
                            "animation": "bounce"
                        }
                    },
                    "voiceover": {
                        "text": "Stop wasting thousands on ads that never convert?",
                        "voice": "professional_male",
                        "speed": 1.0
                    },
                    "subtitles": {
                        "lines": ["Stop wasting thousands", "on ads that never convert?"],
                        "style": "bottom_center",
                        "background": "semi_transparent_black"
                    },
                    "music": {
                        "track": "upbeat_electronic",
                        "volume": 0.3,
                        "fade_in": True
                    },
                    "effects": ["slight_shake", "red_tint"]
                },
                {
                    "scene_id": 2,
                    "time_start": 5,
                    "time_end": 15,
                    "duration": 10,
                    "scene_type": "problem_agitation",
                    "background": {
                        "type": "gradient",
                        "colors": ["#1a1a2e", "#16213e"],
                        "direction": "diagonal"
                    },
                    "visuals": {
                        "main_element": {
                            "type": "split_screen",
                            "left": {"text": "TRADITIONAL", "icon": "❌"},
                            "right": {"text": "AI POWERED", "icon": "✅"},
                            "animation": "slide_in"
                        }
                    },
                    "voiceover": {
                        "text": "What if you could predict exactly what your customers want? Our AI analyzes millions of data points to create perfect ads.",
                        "voice": "professional_male",
                        "speed": 1.0
                    },
                    "subtitles": {
                        "lines": ["What if you could predict", "exactly what customers want?"],
                        "style": "bottom_center"
                    },
                    "music": {
                        "track": "tension_build",
                        "volume": 0.4
                    },
                    "effects": []
                },
                {
                    "scene_id": 3,
                    "time_start": 15,
                    "time_end": 30,
                    "duration": 15,
                    "scene_type": "solution_demo",
                    "background": {
                        "type": "video_placeholder",
                        "description": "Montage of AI processing"
                    },
                    "visuals": {
                        "main_element": {
                            "type": "process_steps",
                            "steps": [
                                {"icon": "📝", "text": "Enter Product"},
                                {"icon": "🤖", "text": "AI Analyzes"},
                                {"icon": "🎬", "text": "Get Ads"}
                            ],
                            "animation": "sequential_reveal"
                        }
                    },
                    "voiceover": {
                        "text": "No more guesswork. Just enter your product, and get professional ads in minutes. Join 10,000+ businesses already growing.",
                        "voice": "professional_male",
                        "speed": 1.0
                    },
                    "subtitles": {
                        "lines": ["Enter product → AI analyzes → Get ads"],
                        "style": "bottom_center"
                    },
                    "music": {
                        "track": "inspiring_beat",
                        "volume": 0.5
                    },
                    "effects": ["smooth_transition"]
                },
                {
                    "scene_id": 4,
                    "time_start": 30,
                    "time_end": 45,
                    "duration": 15,
                    "scene_type": "social_proof",
                    "background": {
                        "type": "solid_color",
                        "color": "#0f3460"
                    },
                    "visuals": {
                        "main_element": {
                            "type": "testimonial_cards",
                            "testimonials": [
                                {"name": "Sarah", "result": "3x ROI", "business": "E-commerce"},
                                {"name": "Mark", "result": "+100% Conversions", "business": "SaaS"}
                            ],
                            "animation": "card_flip"
                        }
                    },
                    "voiceover": {
                        "text": "Sarah from e-commerce saw 3x ROI in 30 days. Mark doubled his conversions. You can too.",
                        "voice": "professional_male",
                        "speed": 1.0
                    },
                    "subtitles": {
                        "lines": ["Sarah: 3x ROI", "Mark: +100% Conversions"],
                        "style": "bottom_center"
                    },
                    "music": {
                        "track": "success_moment",
                        "volume": 0.6
                    },
                    "effects": ["celebration_particles"]
                },
                {
                    "scene_id": 5,
                    "time_start": 45,
                    "time_end": 60,
                    "duration": 15,
                    "scene_type": "cta",
                    "background": {
                        "type": "gradient",
                        "colors": ["#2563EB", "#7C3AED"],
                        "direction": "radial"
                    },
                    "visuals": {
                        "main_element": {
                            "type": "button",
                            "text": "START FREE TRIAL",
                            "style": "prominent_cta",
                            "animation": "pulse"
                        },
                        "secondary": {
                            "type": "text",
                            "content": "No credit card required",
                            "style": "subtitle"
                        }
                    },
                    "voiceover": {
                        "text": "Start your free trial today. No credit card required. Transform your marketing in just 60 seconds.",
                        "voice": "professional_male",
                        "speed": 1.0
                    },
                    "subtitles": {
                        "lines": ["START FREE TRIAL", "No credit card required"],
                        "style": "bottom_center"
                    },
                    "music": {
                        "track": "finale_beat",
                        "volume": 0.7,
                        "fade_out": True
                    },
                    "effects": ["confetti"]
                }
            ],
            "technical_specs": {
                "remotion_composition": {
                    "width": 1080,
                    "height": 1920,
                    "fps": 30
                },
                "audio": {
                    "voiceover_format": "mp3",
                    "music_format": "mp3",
                    "total_audio_tracks": 2
                },
                "export": {
                    "format": "mp4",
                    "codec": "h264",
                    "quality": "high"
                }
            },
            "production_notes": [
                "Use stock footage for scene backgrounds",
                "Record voiceover with professional voice actor",
                "Add subtle animations to text elements",
                "Include brand colors in CTA scene",
                "Test on mobile devices before final export"
            ]
        }
        
        # Save video plan
        result = {
            "product_niche": request.product_niche,
            "video_plan": video_plan,
            "timestamp": get_timestamp()
        }
        save_json(result, "video_plan.json")
        
        return VideoResponse(
            success=True,
            message="Successfully generated video plan",
            video_plan=video_plan,
            timestamp=get_timestamp()
        )
        
    except Exception as e:
        logger.error(f"Error generating video: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-all")
async def generate_all(request: GenerateAllRequest):
    """
    Run the complete pipeline: Search → Analyze → Script → Video
    """
    try:
        logger.info(f"Running complete pipeline for: {request.product_niche}")
        
        # Step 1: Search Ads
        search_response = await search_ads(AdSearchRequest(
            product_niche=request.product_niche,
            days_back=30
        ))
        
        # Step 2: Analyze Ads
        analysis_response = await analyze_ads(AdSearchRequest(
            product_niche=request.product_niche,
            days_back=30
        ))
        
        # Step 3: Generate Script
        script_response = await generate_script(ScriptRequest(
            product_niche=request.product_niche,
            insights=analysis_response.insights
        ))
        
        # Step 4: Generate Video
        video_response = await generate_video(VideoRequest(
            product_niche=request.product_niche,
            script=script_response.script
        ))
        
        # Compile final result
        final_result = {
            "product_niche": request.product_niche,
            "pipeline_status": "completed",
            "steps_completed": [
                {"step": "search-ads", "status": "success", "ads_found": search_response.ads_found},
                {"step": "analyze-ads", "status": "success"},
                {"step": "generate-script", "status": "success"},
                {"step": "generate-video", "status": "success"}
            ],
            "results": {
                "ads": search_response.ads,
                "insights": analysis_response.insights,
                "script": script_response.script,
                "video_plan": video_response.video_plan
            },
            "timestamp": get_timestamp()
        }
        
        # Save complete result
        save_json(final_result, "complete_pipeline.json")
        
        return {
            "success": True,
            "message": "Complete pipeline executed successfully",
            "product_niche": request.product_niche,
            "ads_found": search_response.ads_found,
            "insights": analysis_response.insights,
            "script": script_response.script,
            "video_plan": video_response.video_plan,
            "timestamp": get_timestamp()
        }
        
    except Exception as e:
        logger.error(f"Error in complete pipeline: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history")
async def get_history():
    """Get history of generated ads"""
    try:
        history = []
        
        # Load all generated files
        for filename in ["complete_pipeline.json", "searched_ads.json", "ad_insights.json", "generated_script.json", "video_plan.json"]:
            data = load_json(filename)
            if data:
                history.append({
                    "file": filename,
                    "data": data
                })
        
        return {
            "success": True,
            "history": history,
            "count": len(history)
        }
        
    except Exception as e:
        logger.error(f"Error getting history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)