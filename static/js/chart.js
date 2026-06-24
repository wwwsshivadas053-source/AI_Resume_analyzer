<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<canvas id="atsChart"></canvas>

<script>

const ctx =
document.getElementById('atsChart');

new Chart(ctx, {

type:'line',

data:{

labels:[
{% for item in analyses %}
'{{ item.filename }}',
{% endfor %}
],

datasets:[{

label:'ATS Score',

data:[
{% for item in analyses %}
{{ item.ats_score }},
{% endfor %}
]

}]

}

});

</script>