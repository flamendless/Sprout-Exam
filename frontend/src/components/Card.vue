<script setup>
import { useAdminStore } from "@/stores/admin.js";
import router from "@/router";

const admin = useAdminStore();

defineProps({
	employee_id: {
		type: Number,
		required: true
	},
	first_name: {
		type: String,
		required: true
	},
	last_name: {
		type: String,
		required: true
	}
});

function view_employee(employee_id) {
	router.replace({
		path: `/employee/${employee_id}`
	});
}
</script>

<template>
	<div class="card">
		<span class="pi pi-user user"></span>
		<h4>{{ first_name }} {{ last_name }}</h4>

		<div class="buttons">
			<button @click="view_employee(employee_id)">
				<span class="pi pi-eye"></span>
			</button>
			<button>
				<span class="pi pi-user-edit"></span>
			</button>
			<button @click="admin.delete_employee(employee_id)">
				<span class="pi pi-trash"></span>
			</button>
		</div>
	</div>
</template>

<style scoped>
.card {
	border-style: solid;
	margin: 1em;
	padding: 2em;
	display: flex;
	flex-direction: column;
	align-items: center;
	flex-grow: 1;
}

.card h4 {
	margin: auto;
	text-align: center;
	width: 100%;
}

.card span.user {
	font-size: 4em;
	margin-bottom: 1rem;
}

.card .buttons {
	display: flex;
	flex-direction: row;
	align-items: center;
	justify-content: space-evenly;
	width: 100%;
}

.card .buttons button {
	margin-top: 2em;
	background-color: transparent;
	padding-left: 1.5em;
	padding-right: 1.5em;
	padding-top: 0.5em;
	padding-bottom: 0.5em;
	color: hsla(160, 100%, 37%, 1);
}

.card .buttons button:hover {
	cursor: pointer;
}
</style>
