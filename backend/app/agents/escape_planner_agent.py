"""下班逃离助手智能体"""

import json
import math
from typing import Dict, Any, List, Optional, Tuple
from hello_agents import SimpleAgent
from hello_agents.tools import MCPTool
from ..services.llm_service import get_llm
from ..services.amap_service import get_amap_service
from ..models.schemas import (
    EscapeRequest, EscapePlan, Cinema, Restaurant, MovieShowtime,
    RouteSegment, Location, MovieShowtime
)
from ..config import get_settings


# 模拟电影场次
MOCK_SHOWTIMES = [
    MovieShowtime(time="19:00", movie_name="速度与激情10", duration=120, hall="1号厅", available_seats=45),
    MovieShowtime(time="19:30", movie_name="速度与激情10", duration=120, hall="2号厅", available_seats=32),
    MovieShowtime(time="20:00", movie_name="速度与激情10", duration=120, hall="3号厅", available_seats=58),
]


class EscapePlannerAgent:
    """下班逃离助手"""

    def __init__(self):
        """初始化逃离助手"""
        print("🔄 开始初始化下班逃离助手...")

        try:
            settings = get_settings()

            # 获取 LLM 实例
            print("  - 初始化 LLM 服务...")
            self.llm = get_llm()
            self.llm.timeout = 120

            # 获取高德地图服务
            print("  - 初始化高德地图服务...")
            self.amap_service = get_amap_service()

            # 创建 MCP 工具
            print("  - 创建 MCP 工具...")
            self.amap_tool = MCPTool(
                name="amap",
                description="高德地图服务",
                server_command=["uvx", "amap-mcp-server"],
                env={"AMAP_MAPS_API_KEY": settings.amap_api_key},
                auto_expand=True
            )
            self.amap_tool.expandable = True

            print(f"✅ 下班逃离助手初始化成功")

        except Exception as e:
            print(f"❌ 下班逃离助手初始化失败: {str(e)}")
            import traceback
            traceback.print_exc()
            raise

    def plan_escape(self, request: EscapeRequest) -> EscapePlan:
        """
        生成下班逃离计划

        Args:
            request: 逃离请求

        Returns:
            逃离计划
        """
        try:
            print(f"\n{'='*60}")
            print(f"🚀 开始规划下班逃离路线...")
            print(f"起点: {request.origin}")
            print(f"终点: {request.destination}")
            print(f"下班时间: {request.off_work_time}")
            print(f"城市: {request.city}")
            print(f"{'='*60}\n")

            # 步骤1: 获取起点和终点坐标
            print("📍 步骤1: 获取地址坐标...")
            origin_location = self._geocode(request.origin, request.city)
            dest_location = self._geocode(request.destination, request.city)

            if not origin_location or not dest_location:
                raise ValueError("无法解析起点或终点坐标")

            print(f"   起点坐标: ({origin_location.longitude}, {origin_location.latitude})")
            print(f"   终点坐标: ({dest_location.longitude}, {dest_location.latitude})")

            # 步骤2: 在路径中间寻找电影院
            print("\n🎬 步骤2: 寻找电影院...")
            cinema = self._find_cinema_along_route(
                origin_location,
                dest_location,
                request.city
            )

            # 步骤3: 获取起点到电影院的路线
            print("\n🛣️ 步骤3: 规划路线...")
            segments = []
            total_duration = 0
            total_distance = 0.0
            route_to_cinema = None
            route_to_dest = None

            # 起点 -> 电影院
            if cinema:
                route_to_cinema = self._plan_route(
                    request.origin,
                    cinema.address,
                    request.city
                )
                if route_to_cinema:
                    segments.append(route_to_cinema)
                    total_duration += route_to_cinema.duration
                    total_distance += route_to_cinema.distance
                    print(f"   起点->电影院: {route_to_cinema.distance/1000:.1f}公里, {route_to_cinema.duration/60:.0f}分钟")

                # 电影院 -> 终点
                route_to_dest = self._plan_route(
                    cinema.address,
                    request.destination,
                    request.city
                )
                if route_to_dest:
                    segments.append(route_to_dest)
                    total_duration += route_to_dest.duration
                    total_distance += route_to_dest.distance
                    print(f"   电影院->终点: {route_to_dest.distance/1000:.1f}公里, {route_to_dest.duration/60:.0f}分钟")
            else:
                # 没有电影院，直接规划起点到终点
                route = self._plan_route(request.origin, request.destination, request.city)
                if route:
                    segments.append(route)
                    total_duration = route.duration
                    total_distance = route.distance

            print(f"   总距离: {total_distance/1000:.1f}公里, 总耗时: {total_duration/60:.0f}分钟")

            # 步骤4: 搜索电影院附近餐厅
            print("\n🍽️ 步骤4: 搜索餐厅...")
            restaurant = None
            route_to_restaurant = None
            if cinema:
                restaurant = self._search_nearby_restaurant(
                    cinema.location,
                    request.city
                )
                # 规划从起点到餐厅的路线
                if restaurant:
                    route_to_restaurant = self._plan_route(
                        request.origin,
                        restaurant.address,
                        request.city
                    )
                    if route_to_restaurant:
                        print(f"   起点->餐厅: {route_to_restaurant.distance/1000:.1f}公里, {route_to_restaurant.duration/60:.0f}分钟")

            # 步骤5: 生成时间线
            print("\n📋 步骤5: 生成时间线...")
            # 计算到电影院的时间（秒转分钟）
            travel_to_cinema_min = route_to_cinema.duration // 60 if route_to_cinema else 0
            # 计算到餐厅的时间（秒转分钟）
            travel_to_restaurant_min = route_to_restaurant.duration // 60 if route_to_restaurant else travel_to_cinema_min
            # 计算电影院到终点的时间（秒转分钟）
            travel_from_cinema_min = route_to_dest.duration // 60 if route_to_dest else 0

            timeline = self._generate_timeline(
                request,
                cinema,
                restaurant,
                travel_to_cinema_min,
                travel_to_restaurant_min,
                travel_from_cinema_min
            )

            # 选择电影场次
            selected_showtime = None
            if cinema and cinema.showtimes:
                # 选择19:30的场次（最常见的选择）
                for showtime in cinema.showtimes:
                    if showtime.time == "19:30":
                        selected_showtime = showtime
                        break
                if not selected_showtime:
                    selected_showtime = cinema.showtimes[0]

            # 决定晚餐时间
            dinner_time = ""
            dinner_before_or_after = "after"
            if selected_showtime and restaurant:
                # 电影前吃饭
                dinner_before_or_after = "before"
                # 计算晚餐时间：下班时间后，吃饭大约1小时，要在电影前吃完
                off_hour, off_min = map(int, request.off_work_time.split(":"))
                dinner_time = f"{off_hour + 1}:{off_min:02d}"

            # 构建逃离计划
            escape_plan = EscapePlan(
                origin=request.origin,
                destination=request.destination,
                origin_location=origin_location,
                destination_location=dest_location,
                off_work_time=request.off_work_time,
                total_duration=total_duration // 60,  # 转换为分钟
                total_distance=total_distance,
                route_segments=segments,
                cinema=cinema,
                selected_showtime=selected_showtime,
                dinner_before_or_after=dinner_before_or_after,
                restaurant=restaurant,
                dinner_time=dinner_time,
                timeline=timeline,
                overall_suggestions=self._generate_suggestions(request, cinema, restaurant)
            )

            print(f"\n{'='*60}")
            print(f"✅ 逃离计划生成完成!")
            if cinema:
                print(f"   电影院: {cinema.name}")
            if restaurant:
                print(f"   餐厅: {restaurant.name}")
            print(f"{'='*60}\n")

            return escape_plan

        except Exception as e:
            print(f"❌ 生成逃离计划失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return self._create_fallback_plan(request)

    def _geocode(self, address: str, city: str) -> Optional[Location]:
        """地理编码"""
        try:
            result = self.amap_service.geocode(address, city)
            if result:
                return result
            return None
        except Exception as e:
            print(f"地理编码失败: {str(e)}")
            return None

    def _find_cinema_along_route(
        self,
        origin: Location,
        destination: Location,
        city: str
    ) -> Optional[Cinema]:
        """
        在起点和终点之间寻找电影院
        使用高德地图周边搜索，优先在中间点3km内查找
        """
        try:
            # 计算路径中间点
            mid_longitude = (origin.longitude + destination.longitude) / 2
            mid_latitude = (origin.latitude + destination.latitude) / 2

            print(f"   中间点坐标: ({mid_longitude}, {mid_latitude})")

            # 首先在中间点3km范围内搜索
            print(f"   在中间点3km范围内搜索电影院...")
            cinemas = self._search_cinema(mid_longitude, mid_latitude, city, radius=3000)

            if cinemas:
                print(f"   3km内找到 {len(cinemas)} 家电影院，最近的: {cinemas[0].name}")
                return cinemas[0]

            # 3km没找到，扩大到5km
            print("   3km内无电影院，扩大到5km搜索...")
            cinemas = self._search_cinema(mid_longitude, mid_latitude, city, radius=5000)

            if cinemas:
                print(f"   5km内找到 {len(cinemas)} 家电影院，最近的: {cinemas[0].name}")
                return cinemas[0]

            # 如果中间点没找到，在起点附近找
            print("   中间点附近无电影院，在起点附近搜索...")
            cinemas = self._search_cinema(origin.longitude, origin.latitude, city, radius=5000)
            if cinemas:
                return cinemas[0]

            return None

        except Exception as e:
            print(f"寻找电影院失败: {str(e)}")
            return None

    def _search_cinema(self, longitude: float, latitude: float, city: str, radius: int = 3000) -> List[Cinema]:
        """在指定坐标附近搜索电影院（周边搜索）"""
        try:
            # 使用MCP工具进行周边搜索
            result = self.amap_tool.run({
                "action": "call_tool",
                "tool_name": "maps_around_search",
                "arguments": {
                    "keywords": "电影院",
                    "location": f"{longitude},{latitude}",
                    "radius": str(radius),
                    "sortrule": "distance"
                }
            })

            print(f"   电影院搜索结果: {result[:300]}...")

            # 解析结果，获取所有候选电影院
            cinemas = self._parse_cinema_results(result)

            # 计算每个电影院到中间点的直线距离，并排序
            for cinema in cinemas:
                cinema.distance = self._calculate_distance(
                    longitude, latitude,
                    cinema.location.longitude, cinema.location.latitude
                )

            # 按距离排序
            cinemas.sort(key=lambda x: x.distance if x.distance > 0 else 999999)

            print(f"   找到 {len(cinemas)} 家电影院，距离排序后最近的: {cinemas[0].name if cinemas else '无'}")

            return cinemas

        except Exception as e:
            print(f"搜索电影院失败: {str(e)}")
            return []

    def _calculate_distance(self, lon1: float, lat1: float, lon2: float, lat2: float) -> float:
        """计算两点之间的直线距离（米），使用简化的 Haversine 公式近似"""
        import math
        # 1度经度约等于 111320 * cos(纬度) 米
        # 1度纬度约等于 111320 米
        lat_rad = math.radians((lat1 + lat2) / 2)
        dlat = (lat2 - lat1) * 111320
        dlon = (lon2 - lon1) * 111320 * math.cos(lat_rad)
        return math.sqrt(dlat**2 + dlon**2)

    def _parse_cinema_results(self, result: str) -> List[Cinema]:
        """解析电影院搜索结果"""
        cinemas = []

        try:
            # 尝试解析JSON
            import re
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                # 处理 "return" 包装的情况
                return_data = data.get("return", data)
                pois = return_data.get("pois", [])

                print(f"   解析到 {len(pois)} 个POI")

                for poi in pois[:10]:  # 取前10个
                    try:
                        # 尝试从 POI 中获取 location
                        location_str = poi.get("location", "")
                        lng = 0.0
                        lat = 0.0

                        if location_str and "," in location_str:
                            parts = location_str.split(",")
                            if len(parts) == 2:
                                lng, lat = float(parts[0]), float(parts[1])
                                print(f"   POI '{poi.get('name')}' 坐标: ({lng}, {lat})")
                        else:
                            # 如果POI没有坐标，尝试用地理编码获取
                            address = poi.get("address", poi.get("name", ""))
                            if address:
                                geo = self._geocode(address, None)
                                if geo:
                                    lng, lat = geo.longitude, geo.latitude
                                    print(f"   通过地理编码获取 '{poi.get('name')}' 坐标: ({lng}, {lat})")

                        # 如果仍然没有坐标，使用基于名称的启发式估算
                        if lng == 0.0 and lat == 0.0:
                            print(f"   无法获取 '{poi.get('name')}' 坐标，跳过")
                            continue

                        cinema = Cinema(
                            name=poi.get("name", "未知影院"),
                            address=poi.get("address", ""),
                            location=Location(longitude=lng, latitude=lat),
                            distance=0.0,  # 稍后计算
                            showtimes=MOCK_SHOWTIMES,
                            poi_id=poi.get("id", "")
                        )
                        cinemas.append(cinema)
                    except Exception as ex:
                        print(f"解析影院POI '{poi.get('name')}' 失败: {str(ex)}")
                        continue

        except Exception as e:
            print(f"解析电影院结果失败: {str(e)}")

        return cinemas

    def _plan_route(
        self,
        origin_address: str,
        destination_address: str,
        city: str
    ) -> Optional[RouteSegment]:
        """规划路线"""
        try:
            result = self.amap_service.plan_route(
                origin_address=origin_address,
                destination_address=destination_address,
                origin_city=city,
                destination_city=city,
                route_type="driving"
            )

            if result:
                return RouteSegment(
                    from_place=origin_address,
                    to_place=destination_address,
                    distance=result.get("distance", 0),
                    duration=result.get("duration", 0),
                    route_type="driving",
                    description=f"全程约{result.get('distance', 0)/1000:.1f}公里"
                )

            return None

        except Exception as e:
            print(f"路线规划失败: {str(e)}")
            return None

    def _search_nearby_restaurant(
        self,
        location: Location,
        city: str
    ) -> Optional[Restaurant]:
        """搜索附近的餐厅（基于电影院位置的周边搜索）"""
        try:
            # 使用电影院位置作为中心点，搜索附近3km内的餐厅
            result = self.amap_tool.run({
                "action": "call_tool",
                "tool_name": "maps_around_search",
                "arguments": {
                    "keywords": "餐厅",
                    "location": f"{location.longitude},{location.latitude}",
                    "radius": "3000",
                    "sortrule": "distance"
                }
            })

            print(f"   餐厅搜索结果: {result[:300]}...")

            restaurants = self._parse_restaurant_result(result, city)

            # 计算每个餐厅到电影院位置的直线距离
            for restaurant in restaurants:
                if restaurant.location:
                    restaurant.distance = self._calculate_distance(
                        location.longitude, location.latitude,
                        restaurant.location.longitude, restaurant.location.latitude
                    )

            if restaurants:
                # 按距离排序，只保留3公里内的
                restaurants.sort(key=lambda x: x.distance if x.distance > 0 else 999999)
                nearby = [r for r in restaurants if r.distance <= 3000]
                if nearby:
                    print(f"   3公里内找到 {len(nearby)} 家餐厅，最近的: {nearby[0].name}")
                    return nearby[0]
                # 如果3公里内没有，返回最近的
                if restaurants:
                    print(f"   3公里内无餐厅，返回最近的: {restaurants[0].name}，距离 {restaurants[0].distance:.0f}米")
                    return restaurants[0]
            return None

        except Exception as e:
            print(f"搜索餐厅失败: {str(e)}")
            return None

    def _parse_restaurant_result(self, result: str, city: str) -> List[Restaurant]:
        """解析餐厅搜索结果"""
        restaurants = []
        try:
            import re
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                # 处理 "return" 包装的情况
                return_data = data.get("return", data)
                pois = return_data.get("pois", [])

                print(f"   解析到 {len(pois)} 个餐厅POI")

                for poi in pois[:10]:  # 取前10个
                    try:
                        location_str = poi.get("location", "")
                        lng = 0.0
                        lat = 0.0

                        if location_str and "," in location_str:
                            parts = location_str.split(",")
                            if len(parts) == 2:
                                lng, lat = float(parts[0]), float(parts[1])
                        else:
                            # 如果POI没有坐标，尝试用地理编码获取
                            address = poi.get("address", poi.get("name", ""))
                            if address:
                                geo = self._geocode(address, city)
                                if geo:
                                    lng, lat = geo.longitude, geo.latitude
                                    print(f"   通过地理编码获取 '{poi.get('name')}' 坐标: ({lng}, {lat})")

                        if lng == 0.0 and lat == 0.0:
                            print(f"   无法获取 '{poi.get('name')}' 坐标，跳过")
                            continue

                        restaurant = Restaurant(
                            name=poi.get("name", "未知餐厅"),
                            address=poi.get("address", ""),
                            location=Location(longitude=lng, latitude=lat),
                            cuisine=poi.get("type", ""),
                            price_range="",
                            rating=float(poi.get("rating", 0)) if poi.get("rating") else None,
                            distance=0.0,  # 稍后计算
                            estimated_cost=80
                        )
                        restaurants.append(restaurant)
                    except Exception as ex:
                        print(f"解析餐厅POI失败: {str(ex)}")
                        continue

        except Exception as e:
            print(f"解析餐厅结果失败: {str(e)}")

        return restaurants

    def _generate_timeline(
        self,
        request: EscapeRequest,
        cinema: Optional[Cinema],
        restaurant: Optional[Restaurant],
        travel_to_cinema_minutes: int = 0,
        travel_to_restaurant_minutes: int = 0,
        travel_from_cinema_minutes: int = 0
    ) -> List[Dict[str, Any]]:
        """生成详细时间线"""
        timeline = []
        off_hour, off_min = map(int, request.off_work_time.split(":"))
        current_minutes = off_hour * 60 + off_min

        # 下班
        timeline.append({
            "time": request.off_work_time,
            "event": "下班",
            "location": request.origin,
            "description": "收拾东西，准备出发"
        })

        # 如果有餐厅且电影前进食
        if restaurant and cinema:
            # 到达餐厅时间
            arrive_restaurant_minutes = current_minutes + travel_to_restaurant_minutes
            timeline.append({
                "time": f"{arrive_restaurant_minutes // 60}:{arrive_restaurant_minutes % 60:02d}",
                "event": "晚餐",
                "location": restaurant.name,
                "description": f"享用晚餐"
            })
            # 计算从餐厅到电影院的时间
            current_minutes = arrive_restaurant_minutes + 60  # 吃饭约1小时
            # 加上从餐厅到电影院的路上时间（简化处理，用总时间减去已用时间）
            current_minutes += 10  # 假设从餐厅到电影院10分钟
        elif cinema:
            # 直接去电影院
            current_minutes += travel_to_cinema_minutes

        # 前往电影院 - 根据选择的场次反推
        if cinema and cinema.showtimes:
            # 选择电影场次
            showtime = cinema.showtimes[0]
            show_hour, show_min = map(int, showtime.time.split(":"))
            showtime_minutes = show_hour * 60 + show_min

            # 计算到达时间（电影前15分钟取票）
            arrive_minutes = showtime_minutes - 15

            # 如果计算出的到达时间比当前时间早，用当前时间+路上时间
            if arrive_minutes <= current_minutes:
                # 需要提前出发才能赶上电影
                arrive_minutes = current_minutes + 5

            timeline.append({
                "time": f"{arrive_minutes // 60}:{arrive_minutes % 60:02d}",
                "event": "到达电影院",
                "location": cinema.name,
                "description": f"取票，准备观影"
            })

            # 电影开场
            timeline.append({
                "time": showtime.time,
                "event": "电影开场",
                "location": cinema.name,
                "description": f"观看《{showtime.movie_name}》，片长{showtime.duration}分钟"
            })

            # 电影结束
            end_minutes = showtime_minutes + showtime.duration
            timeline.append({
                "time": f"{end_minutes // 60}:{end_minutes % 60:02d}",
                "event": "电影结束",
                "location": cinema.name,
                "description": "返回家中或继续其他活动"
            })

            # 到家
            arrive_home_minutes = end_minutes + travel_from_cinema_minutes
            timeline.append({
                "time": f"{arrive_home_minutes // 60}:{arrive_home_minutes % 60:02d}",
                "event": "到家",
                "location": request.destination,
                "description": "回家休息"
            })

        return timeline

    def _add_minutes(self, time_str: str, minutes: int) -> str:
        """时间加分钟"""
        try:
            hour, minute = map(int, time_str.split(":"))
            total_minutes = hour * 60 + minute + minutes
            new_hour = (total_minutes // 60) % 24
            new_minute = total_minutes % 60
            return f"{new_hour}:{new_minute:02d}"
        except:
            return time_str

    def _generate_suggestions(
        self,
        request: EscapeRequest,
        cinema: Optional[Cinema],
        restaurant: Optional[Restaurant]
    ) -> str:
        """生成建议"""
        suggestions = []

        suggestions.append("下班后直接出发，避开晚高峰")
        if cinema:
            suggestions.append(f"建议提前在网上订票，选择{cinema.name}")
        if restaurant:
            suggestions.append("晚餐可以选择就近的餐厅，用餐时间控制在1小时内")
        suggestions.append("观影结束后如果时间允许，可以再享用一顿夜宵")

        return "；".join(suggestions)

    def _create_fallback_plan(self, request: EscapeRequest) -> EscapePlan:
        """创建备用计划"""
        return EscapePlan(
            origin=request.origin,
            destination=request.destination,
            off_work_time=request.off_work_time,
            total_duration=60,
            total_distance=15000,
            route_segments=[
                RouteSegment(
                    from_place=request.origin,
                    to_place="附近电影院",
                    distance=5000,
                    duration=1800,
                    route_type="driving",
                    description="约5公里"
                )
            ],
            cinema=Cinema(
                name="万达影城(上海五角场店)",
                address="上海市杨浦区国宾路58号万达广场4层",
                location=Location(longitude=121.514745, latitude=31.300557),
                distance=500,
                showtimes=MOCK_SHOWTIMES
            ),
            selected_showtime=MOCK_SHOWTIMES[1],
            dinner_before_or_after="before",
            restaurant=Restaurant(
                name="绿茶餐厅(五角场店)",
                address="上海市杨浦区邯郸路100号",
                location=Location(longitude=121.5100, latitude=31.2950),
                cuisine="江浙菜",
                price_range="60-80元",
                rating=4.5,
                distance=100,
                estimated_cost=70
            ),
            dinner_time="18:45",
            timeline=[
                {
                    "time": request.off_work_time,
                    "event": "下班",
                    "location": request.origin,
                    "description": "收拾东西，准备出发"
                },
                {
                    "time": "18:30",
                    "event": "晚餐",
                    "location": "绿茶餐厅(五角场店)",
                    "description": "享用晚餐"
                },
                {
                    "time": "19:30",
                    "event": "电影开场",
                    "location": "万达影城(上海五角场店)",
                    "description": "观看《速度与激情10》，片长120分钟"
                },
                {
                    "time": "21:30",
                    "event": "电影结束",
                    "location": "万达影城(上海五角场店)",
                    "description": "返回家中"
                }
            ],
            overall_suggestions="建议提前出发，避开晚高峰；电影结束后可乘地铁回家"
        )


# 全局实例
_escape_planner_agent = None


def get_escape_planner_agent() -> EscapePlannerAgent:
    """获取逃离规划智能体实例"""
    global _escape_planner_agent

    if _escape_planner_agent is None:
        _escape_planner_agent = EscapePlannerAgent()

    return _escape_planner_agent
