$ ->
    map = new BMap.Map("allmap")
    point = new BMap.Point(121.531405, 31.215183)
    map.centerAndZoom(point, 14)
    map.enableScrollWheelZoom(true)
    map.setCurrentCity("北京")
    top_left_control = new BMap.ScaleControl({anchor: BMAP_ANCHOR_TOP_LEFT})
    map.addControl(top_left_control)
    top_left_navigation = new BMap.NavigationControl()
    map.addControl(top_left_navigation)

    addMarker = (job) ->
        point = new BMap.Point(job['lng'], job['lat'])
        marker = new BMap.Marker(point)
        map.addOverlay(marker)

        sContent ="
<p>
    职位：#{job.title} <br/>
    公司：#{job.company_name} #{job.company_size} <br/>
    资金：#{job.stage} <br/>
    地址：#{job.location} <br/>
    待遇：#{job.salary} <br/>
    来源：<a href='http://www.lagou.com/jobs/#{job.jid}.html'>拉勾网</a>
</p>
"
        infoWindow = new BMap.InfoWindow(sContent)
        marker.addEventListener "click", ->
            this.openInfoWindow(infoWindow)
            document.getElementById('imgDemo').onload = ->
                infoWindow.redraw()

    $.getJSON('/api/jobs').success (data) ->
        return true if not data.error? or data.error != 0

        for job in data['items']
            addMarker(job)
