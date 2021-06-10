$.init = function () {
    $.ajax({
        type: "POST",
        url: "/get_chart/",
        async: true,
        success: function (data) {
            data = JSON.parse(data)
            console.log(data)
            $.agechart(data.age)
            $.sexchart(data.sex)
            $.dischart(data.dis)
            $.areachart(data.area)
        }
    })
}

$.init()
var myage = echarts.init(document.getElementById('age'));
var mysex = echarts.init(document.getElementById('sex'));
var mydis = echarts.init(document.getElementById('dis'));
var myarea = echarts.init(document.getElementById('area'));

var colors = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc']
$.areachart = function (d) {
    var option = {
        title: {
            text: '解剖标注统计',
            x: "center"
        },
        tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        color: colors,
        series: [
            {
                name: '解剖名称',
                type: 'pie',
                radius: '60%',
                //center: ['40%', '50%'],
                data: d,
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]

    };
    myarea.setOption(option);
}

$.dischart = function (d) {
    var option = {
        title: {
            text: '疾病标注统计',
            x: "center"
        },
        tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        color: colors,
        series: [
            {
                name: '疾病名称',
                type: 'pie',
                radius: '60%',
                //center: ['40%', '50%'],
                data: d,
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]

    };
    mydis.setOption(option);
}

$.sexchart = function (d) {
    var option = {
        title: {
            text: '患者性别分布',
            textAlign: "left",
            x: 'center',
         },
         tooltip: {
            trigger: 'item'
        },
        color: ['#FF6EB4','#1874CD'],
        series: [
            {
                name: '患者数量',
                type: 'pie',
                radius: '60%',
                data: [
                    {value: d.ydata[0], name: d.xdata[0]},
                    {value: d.ydata[1], name: d.xdata[1]},
                ],
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]

    };
    mysex.setOption(option);
}

$.agechart = function (d) {
    var option = {
        title: {
            text: '患者随年龄分布',
            textAlign: "left",
            x: 'center',
         },
        tooltip: {
            trigger: 'axis',
        },
        legend: {
            data: ['患者年龄']
        },
        xAxis: {
            data: d.xdata
        },
        yAxis: {},
        series: [{
            name: '患者数量',
            type: 'line',
            data: d.ydata
        }]

    };
    myage.setOption(option);
}

