function main(){
    const plotConfigs = {}
    const lazyLoad = async (chart_name)=>{
        if (plotConfigs[chart_name] == undefined){
            plotConfigs[chart_name] = (await axios.get('/charts/' + chart_name)).data
        }
        return plotConfigs[chart_name]
    }

    const { createApp } = Vue
    createApp({
        data() {
            return {
                selected: null,
                charts: null
            }
        },
        methods: {
            async select(chart_name){
                this.selected = chart_name
                if (this.chart){
                    this.chart.destroy()
                }
                const config = await lazyLoad(chart_name)
                this.chart = new Chart(this.$refs.canvas, config)
            }
        },
        async created(){
            let charts = (await axios.get('/charts/')).data
            this.charts = charts
            Vue.nextTick(()=>this.select(charts[0]))
        }
    }).mount('#app')  
}
document.addEventListener("DOMContentLoaded",main);