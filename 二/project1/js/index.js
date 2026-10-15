(function() {
    // 1. 折线图: 粮食/蔬菜/水果产量趋势
    const lineChart = echarts.init(document.getElementById('trend-line'));
    lineChart.setOption({
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' }, backgroundColor: '#FEFFED', borderColor: '#BAD19C' },
        legend: { data: ['粮食总产', '蔬菜总产', '水果总产'], bottom: 0, left: 'center', icon: 'circle', textStyle: { color: '#3D6030' }, itemWidth: 20, itemHeight: 10 },
        grid: { top: 35, left: 50, right: 20, bottom: 30, containLabel: true },
        xAxis: { type: 'category', data: ['2020', '2021', '2022', '2023', '2024'], axisLabel: { fontWeight: 500, color: '#497536' } },
        yAxis: { type: 'value', name: '万吨', nameTextStyle: { color: '#628447' }, splitLine: { lineStyle: { color: '#CFE2B0', type: 'dashed' } } },
        series: [
            { name: '粮食总产', type: 'line', smooth: true, data: [66949, 68285, 68653, 69541, 70800], lineStyle: { width: 2.5, color: '#7AA758' }, symbol: 'circle', areaStyle: { opacity: 0.15, color: '#B1CF8A' } },
            { name: '蔬菜总产', type: 'line', smooth: true, data: [72492, 74856, 77500, 79822, 83500], lineStyle: { width: 2, color: '#C7B45B' }, symbol: 'diamond' },
            { name: '水果总产', type: 'line', smooth: true, data: [28692, 29611, 30998, 32423, 34680], lineStyle: { width: 2, color: '#DA8A62' }, symbol: 'roundRect' }
        ]
    });

    // 2. 饼图 种植结构（水稻、玉米、小麦、大豆、薯类）
    const pieChart = echarts.init(document.getElementById('pie-structure'));
    pieChart.setOption({
        tooltip: { trigger: 'item', formatter: '{b}: {d}%' },
        legend: { orient: 'vertical', left: 'left', textStyle: { color: '#396230' }, itemWidth: 18, itemHeight: 10 },
        series: [{
            type: 'pie', radius: ['40%', '65%'], center: ['55%', '55%'],
            data: [
                { name: '水稻', value: 33.8, itemStyle: { color: '#A9CD84' } },
                { name: '玉米', value: 29.5, itemStyle: { color: '#EDC16A' } },
                { name: '小麦', value: 21.2, itemStyle: { color: '#D1B079' } },
                { name: '大豆', value: 8.2, itemStyle: { color: '#9DC06E' } },
                { name: '薯类杂粮', value: 7.3, itemStyle: { color: '#BCD691' } }
            ],
            label: { show: true, formatter: '{b}', color: '#38662A', fontWeight: 500, fontSize: 10 },
            itemStyle: { borderRadius: 8, borderColor: '#F6FCE9', borderWidth: 2 }
        }]
    });

    // 3. 地图核心：省份农业产值数据（单位：亿元）
    const agriGDP = {
        '山东省': 11268, '河南省': 10098, '江苏省': 8225, '四川省': 7295, '河北省': 6920, '湖南省': 6525,
        '湖北省': 6195, '广东省': 6124, '黑龙江省': 5905, '安徽省': 5560, '广西壮族自治区': 4780, '云南省': 4350,
        '江西省': 4090, '辽宁省': 3820, '福建省': 3720, '陕西省': 3350, '山西省': 2980, '贵州省': 2760,
        '吉林省': 3580, '甘肃省': 2180, '内蒙古自治区': 3100, '新疆维吾尔自治区': 2950, '重庆市': 1950,
        '天津市': 485, '北京市': 385, '上海市': 318, '青海省': 420, '宁夏回族自治区': 620,
        '海南省': 1280, '西藏自治区': 210, '浙江省': 3430
    };
    
    const mapChart = echarts.init(document.getElementById('agriculture-map'));
    const mapData = Object.entries(agriGDP).map(([name, value]) => ({ name, value }));
    const maxVal = Math.max(...Object.values(agriGDP));
    const minVal = Math.min(...Object.values(agriGDP));
    
    mapChart.setOption({
        tooltip: { trigger: 'item', formatter: '{b}<br/>🌾 农业总产值: {c} 亿元', backgroundColor: '#FDF7E0', borderColor: '#BED79A' },
        visualMap: {
            min: minVal,
            max: maxVal,
            left: 15,
            bottom: 15,
            calculable: true,
            inRange: { color: ['#E9F5D3', '#C4DEA4', '#91AF71', '#638A46'] },
            textStyle: { color: '#366129', fontSize: 10 },
            formatter: '{value} 亿元'
        },
        series: [{
            name: '农业产值分布', type: 'map', map: 'china', roam: true, zoom: 1.1,
            itemStyle: { normal: { borderColor: '#DFECC3', borderWidth: 0.6, areaColor: '#E2EFCC' },
                         emphasis: { label: { show: true }, areaColor: '#C6E2A3' } },
            label: { normal: { show: false }, emphasis: { show: true, color: '#2B5620', fontSize: 10 } },
            data: mapData,
            aspectScale: 0.85
        }],
        backgroundColor: 'transparent'
    });
    
    window.addEventListener('resize', () => mapChart.resize());

    // 4. 横向柱状图 TOP6 省份产值
    const barChart = echarts.init(document.getElementById('bar-ranking'));
    barChart.setOption({
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' }, formatter: '{b}: {c} 亿元' },
        grid: { containLabel: true, left: 85, top: 18, right: 15, bottom: 18 },
        xAxis: { type: 'value', name: '亿元', axisLabel: { color: '#54823B', fontSize: 10 }, splitLine: { lineStyle: { color: '#CDE4AE' } } },
        yAxis: { type: 'category', data: ['山东省', '河南省', '江苏省', '四川省', '河北省', '湖南省'], axisLabel: { fontWeight: 500, color: '#38662A', fontSize: 11 } },
        series: [{
            name: '农业产值', type: 'bar', data: [11268, 10098, 8225, 7295, 6920, 6525],
            itemStyle: {
                borderRadius: [0, 10, 10, 0],
                color: { type: 'linear', x: 0, y: 0, x2: 1, y2: 0, colorStops: [{ offset: 0, color: '#9ABB74' }, { offset: 1, color: '#CBE2AA' }] },
                shadowColor: 'rgba(100,120,50,0.15)'
            },
            label: { show: true, position: 'right', fontWeight: 'bold', color: '#2E6320', fontSize: 10, formatter: '{c} 亿' }
        }]
    });

    // 5. 雷达图：农业资源及生态效率指标
    const radarChart = echarts.init(document.getElementById('radar-modern'));
    radarChart.setOption({
        radar: {
            indicator: [
                { name: '机械化水平', max: 100 },
                { name: '数字农业', max: 100 },
                { name: '绿色占比', max: 100 },
                { name: '节水灌溉', max: 100 },
                { name: '生态指数', max: 100 },
                { name: '科技贡献', max: 100 }
            ],
            shape: 'circle', radius: '60%',
            name: { textStyle: { color: '#466F34', fontSize: 9, fontWeight: 500 } },
            splitArea: { areaStyle: { color: ['rgba(180, 208, 122, 0.2)', 'rgba(207, 228, 153, 0.25)'] } },
            axisLine: { lineStyle: { color: '#B8D697' } }
        },
        series: [{
            type: 'radar', data: [{ value: [86, 71, 68, 82, 84, 79], name: '现代农业指标' }],
            areaStyle: { color: 'rgba(145, 175, 113, 0.35)' },
            lineStyle: { width: 2, color: '#6A9648' },
            itemStyle: { color: '#56843A' },
            symbol: 'circle', symbolSize: 5
        }],
        legend: { show: true, data: ['综合评估'], left: 'center', bottom: 0, icon: 'circle', textStyle: { color: '#427330', fontSize: 10 } }
    });

    // 全局自适应
    const allCharts = [lineChart, pieChart, mapChart, barChart, radarChart];
    window.addEventListener('resize', () => {
        allCharts.forEach(ch => ch && ch.resize());
    });
    
    // 地图交互友好
    mapChart.on('click', (params) => {
        if (params.componentType === 'series' && params.name) {
            console.log(`🌱 农业地理: ${params.name} 产值 ${params.value} 亿元`);
        }
    });
})();