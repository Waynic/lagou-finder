/**
 * Created by qimi on 2016/5/9.
 */
(function() {
    $(function() {
        var map = new BMap.Map("allmap");          // 创建地图实例
        var point = new BMap.Point(116.404, 39.915);  // 创建点坐标
        map.centerAndZoom(point, 15);                 // 初始化地图，设置中心点坐标和地图级别
        var top_left_control = new BMap.ScaleControl({
            anchor: BMAP_ANCHOR_TOP_LEFT
        });// 左上角，添加比例尺
	    var top_left_navigation = new BMap.NavigationControl();  //左上角，添加默认缩放平移控件
        map.addControl(top_left_control);
        map.addControl(top_left_navigation);
        map.setCurrentCity("北京");          // 设置地图显示的城市 此项是必须设置的
	    map.enableScrollWheelZoom(true);     //开启鼠标滚轮缩放
    })
})();