<script setup>
defineProps({
	first_name: {
		type: String,
		required: true
	},
	last_name: {
		type: String,
		required: true
	},
})
</script>

<template>
	<div class="card">
		<h4>{{first_name}} {{last_name}}</h4>
		<div class="buttons">
			<button>
				<span class="pi pi-list"></span>
			</button>
		</div>
	</div>
</template>

<style scoped>
.card {
	border-style: solid;
	margin: 1em;
	padding: 2em;
	width: 100%;
}

.card h4 {
	margin: auto;
	text-align: center;
	width: 100%;
}

.card .buttons button {
	margin-top: 2em;
	background-color: transparent;
	color: hsla(160, 100%, 37%, 1);
}
</style>
