"""高德地图MCP服务封装"""

from typing import List, Dict, Any, Optional
from hello_agents.tools import MCPTool
from ..config import get_settings
from ..models.schemas import Location, POIInfo, WeatherInfo

# 全局MCP工具实例
_amap_mcp_tool = None


def get_amap_mcp_tool() -> MCPTool:
    """
    获取高德地图MCP工具实例(单例模式)
    
    Returns:
        MCPTool实例
    """
    global _amap_mcp_tool
    
    if _amap_mcp_tool is None:
        settings = get_settings()
        
        if not settings.amap_api_key:
            raise ValueError("高德地图API Key未配置,请在.env文件中设置AMAP_API_KEY")
        
        # 创建MCP工具
        _amap_mcp_tool = MCPTool(
            name="amap",
            description="高德地图服务,支持POI搜索、路线规划、天气查询等功能",
            server_command=["uvx", "amap-mcp-server"],
            env={"AMAP_MAPS_API_KEY": settings.amap_api_key},
            auto_expand=True  # 自动展开为独立工具
        )
        
        print(f"✅ 高德地图MCP工具初始化成功")
        print(f"   工具数量: {len(_amap_mcp_tool._available_tools)}")
        
        # 打印可用工具列表
        if _amap_mcp_tool._available_tools:
            print("   可用工具:")
            for tool in _amap_mcp_tool._available_tools[:5]:  # 只打印前5个
                print(f"     - {tool.get('name', 'unknown')}")
            if len(_amap_mcp_tool._available_tools) > 5:
                print(f"     ... 还有 {len(_amap_mcp_tool._available_tools) - 5} 个工具")
    
    return _amap_mcp_tool


class AmapService:
    """高德地图服务封装类"""
    
    def __init__(self):
        """初始化服务"""
        self.mcp_tool = get_amap_mcp_tool()
    
    def search_poi(self, keywords: str, city: str, citylimit: bool = True) -> List[POIInfo]:
        """
        搜索POI
        
        Args:
            keywords: 搜索关键词
            city: 城市
            citylimit: 是否限制在城市范围内
            
        Returns:
            POI信息列表
        """
        try:
            # 调用MCP工具
            result = self.mcp_tool.run({
                "action": "call_tool",
                "tool_name": "maps_text_search",
                "arguments": {
                    "keywords": keywords,
                    "city": city,
                    "citylimit": str(citylimit).lower()
                }
            })
            
            # 解析结果
            # 注意: MCP工具返回的是字符串,需要解析
            # 这里简化处理,实际应该解析JSON
            print(f"POI搜索结果: {result[:200]}...")  # 打印前200字符
            
            # TODO: 解析实际的POI数据
            return []
            
        except Exception as e:
            print(f"❌ POI搜索失败: {str(e)}")
            return []
    
    def get_weather(self, city: str) -> List[WeatherInfo]:
        """
        查询天气
        
        Args:
            city: 城市名称
            
        Returns:
            天气信息列表
        """
        try:
            # 调用MCP工具
            result = self.mcp_tool.run({
                "action": "call_tool",
                "tool_name": "maps_weather",
                "arguments": {
                    "city": city
                }
            })
            
            print(f"天气查询结果: {result[:200]}...")
            
            # TODO: 解析实际的天气数据
            return []
            
        except Exception as e:
            print(f"❌ 天气查询失败: {str(e)}")
            return []
    
    def plan_route(
        self,
        origin_address: str,
        destination_address: str,
        origin_city: Optional[str] = None,
        destination_city: Optional[str] = None,
        route_type: str = "walking"
    ) -> Dict[str, Any]:
        """
        规划路线
        
        Args:
            origin_address: 起点地址
            destination_address: 终点地址
            origin_city: 起点城市
            destination_city: 终点城市
            route_type: 路线类型 (walking/driving/transit)
            
        Returns:
            路线信息
        """
        try:
            # 根据路线类型选择工具
            tool_map = {
                "walking": "maps_direction_walking_by_address",
                "driving": "maps_direction_driving_by_address",
                "transit": "maps_direction_transit_integrated_by_address"
            }
            
            tool_name = tool_map.get(route_type, "maps_direction_walking_by_address")
            
            # 构建参数
            arguments = {
                "origin_address": origin_address,
                "destination_address": destination_address
            }
            
            # 公共交通需要城市参数
            if route_type == "transit":
                if origin_city:
                    arguments["origin_city"] = origin_city
                if destination_city:
                    arguments["destination_city"] = destination_city
            else:
                # 其他路线类型也可以提供城市参数提高准确性
                if origin_city:
                    arguments["origin_city"] = origin_city
                if destination_city:
                    arguments["destination_city"] = destination_city
            
            # 调用MCP工具
            result = self.mcp_tool.run({
                "action": "call_tool",
                "tool_name": tool_name,
                "arguments": arguments
            })

            print(f"路线规划结果: {result[:300]}...")

            # 解析路线数据
            import json
            import re

            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            if json_match:
                try:
                    data = json.loads(json_match.group())
                    # 处理 "return" 包装的情况
                    route_data = data.get("return", data)
                    route = route_data.get("route", {})

                    # 提取距离和耗时
                    # 驾乘路线格式: route.route.paths[0].distance / duration
                    # 步行路线格式: route.routes[0].distance / duration
                    paths = route.get("paths", [])
                    if paths and len(paths) > 0:
                        distance = int(paths[0].get("distance", 0))
                        duration = int(paths[0].get("duration", 0))
                        return {"distance": distance, "duration": duration}

                    # 尝试其他格式
                    routes = route.get("routes", [])
                    if routes and len(routes) > 0:
                        distance = int(routes[0].get("distance", 0))
                        duration = int(routes[0].get("duration", 0))
                        return {"distance": distance, "duration": duration}

                except (json.JSONDecodeError, ValueError, KeyError) as e:
                    print(f"解析路线数据失败: {str(e)}")

            return {}
            
        except Exception as e:
            print(f"❌ 路线规划失败: {str(e)}")
            return {}
    
    def geocode(self, address: str, city: Optional[str] = None) -> Optional[Location]:
        """
        地理编码(地址转坐标)

        Args:
            address: 地址
            city: 城市

        Returns:
            经纬度坐标
        """
        try:
            arguments = {"address": address}
            if city:
                arguments["city"] = city

            result = self.mcp_tool.run({
                "action": "call_tool",
                "tool_name": "maps_geo",
                "arguments": arguments
            })

            print(f"地理编码结果: {result[:200]}...")

            # 解析JSON结果
            import json
            import re

            json_match = re.search(r'\[.*\]', result, re.DOTALL)
            if not json_match:
                json_match = re.search(r'\{.*\}', result, re.DOTALL)

            if json_match:
                try:
                    data = json.loads(json_match.group())
                    # 如果是列表，直接使用；如果是字典，取return或geocodes
                    if isinstance(data, list):
                        geocodes = data
                    else:
                        geocodes = data.get("return", data.get("geocodes", []))

                    if geocodes and len(geocodes) > 0:
                        geo = geocodes[0]
                        location_str = geo.get("location", "")
                        if location_str and "," in location_str:
                            lng, lat = map(float, location_str.split(","))
                            return Location(longitude=lng, latitude=lat)
                except json.JSONDecodeError:
                    pass

            # 如果解析失败，返回一个默认坐标
            return Location(longitude=121.4737, latitude=31.2304)  # 上海默认坐标

        except Exception as e:
            print(f"❌ 地理编码失败: {str(e)}")
            # 返回默认坐标
            return Location(longitude=121.4737, latitude=31.2304)  # 上海默认坐标

    def get_poi_detail(self, poi_id: str) -> Dict[str, Any]:
        """
        获取POI详情

        Args:
            poi_id: POI ID

        Returns:
            POI详情信息
        """
        try:
            result = self.mcp_tool.run({
                "action": "call_tool",
                "tool_name": "maps_search_detail",
                "arguments": {
                    "id": poi_id
                }
            })

            print(f"POI详情结果: {result[:200]}...")

            # 解析结果并提取图片
            import json
            import re

            # 尝试从结果中提取JSON
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return data

            return {"raw": result}

        except Exception as e:
            print(f"❌ 获取POI详情失败: {str(e)}")
            return {}

    def plan_transit_route_direct(
        self,
        origin: str,
        destination: str,
        city: str
    ) -> Dict[str, Any]:
        """
        直接调用高德公交路线API（绕过MCP）

        Args:
            origin: 起点坐标 "经度,纬度"
            destination: 终点坐标 "经度,纬度"
            city: 城市名称

        Returns:
            公交路线数据
        """
        try:
            import requests

            response = requests.get(
                "https://restapi.amap.com/v3/direction/transit/integrated",
                params={
                    "key": self.mcp_tool.env.get("AMAP_MAPS_API_KEY"),
                    "origin": origin,
                    "destination": destination,
                    "city": city,
                    "cityd": city
                },
                timeout=10
            )

            data = response.json()

            print(f"   公交API返回: {str(data)[:500]}...")

            if data.get("status") != "1":
                return {"error": f"公交路线查询失败: {data.get('info', '')}"}

            return data

        except Exception as e:
            print(f"❌ 直接调用公交API失败: {str(e)}")
            return {"error": str(e)}


# 创建全局服务实例
_amap_service = None


def get_amap_service() -> AmapService:
    """获取高德地图服务实例(单例模式)"""
    global _amap_service
    
    if _amap_service is None:
        _amap_service = AmapService()
    
    return _amap_service

