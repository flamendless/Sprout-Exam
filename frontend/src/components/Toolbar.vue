<script setup>
import { useAdminStore } from "@/stores/admin.js";
import { useAuthStore } from "@/stores/auth.js";

const admin = useAdminStore();
const auth = useAuthStore();
</script>

<template>
	<div class="toolbar">
		<button @click="admin.get_employees">
			<span class="pi pi-refresh"></span>
		</button>

		<button @click="admin.toggle_create_form">
			<span class="pi pi-plus-circle"> </span>
		</button>

		<button @click="admin.toggle_layout">
			<span v-if="admin.layout == 'grid'" class="pi pi-list"> </span>
			<span v-else="admin.layout == 'list'" class="pi pi-table"> </span>
		</button>

		<button @click="auth.logout">
			<span class="pi pi-sign-out"></span>
		</button>
	</div>
</template>

<style scoped>
.toolbar {
	display: flex;
	flex-direction: row;
	align-items: center;
	justify-content: space-evenly;
	margin: 1em;
	padding: 1em;
	border-style: solid;
	min-width: 512px;
}

.toolbar button {
	margin: auto;
	padding-top: 1vh;
	padding-bottom: 1vh;
	padding-left: 2vw;
	padding-right: 2vw;
	border-radius: 12px;
	background-color: transparent;
	color: hsla(160, 100%, 37%, 1);
	border-color: white;
}

.toolbar button:hover {
	cursor: pointer;
}
</style>
