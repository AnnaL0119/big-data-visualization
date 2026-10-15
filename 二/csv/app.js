const myChart = echarts.init(document.getElementById('mainChart'));

fetch('data_process.csv')
    .then(res => res.text())
    .then(text => {
        const lines = text.split('\n').slice(1);
        const cityMap = {};

        lines.forEach(line => {
            const cols = line.split(',');
            if (cols.length < 8) return;
            const city = cols[1] || '未知';
            cityMap[city] = (cityMap[city] || 0) + 1;
        });

        // 取岗位数前5的城市
        const sorted = Object.entries(cityMap).sort((a, b) => b[1] - a[1]);
        const top5 = sorted.slice(0, 5);

        const xData = top5.map(item => item[0]);
        const yData = top5.map(item => item[1]);

        // 浅蓝配色柱状图
        myChart.setOption({
            tooltip: { trigger: 'axis' },
            grid: { left: '12%', right: '10%', bottom: '15%', top: '15%' },
            xAxis: {
                type: 'category',
                data: xData,
                axisLabel: { color: '#fff' },
                axisLine: { lineStyle: { color: '#aaa' } }
            },
            yAxis: {
                type: 'value',
                axisLabel: { color: '#fff' },
                axisLine: { lineStyle: { color: '#aaa' } }
            },
            series: [{
                type: 'bar',
                data: yData,
                itemStyle: { color: '#91d5ff' }, // 浅蓝
                emphasis: { itemStyle: { color: '#69b8ff' } }
            }]
        });
    });