<script setup>
import { ref, computed } from "vue";
import CONST from "@/const.js";
import Card from "@/components/Card.vue";
import Toolbar from "@/components/Toolbar.vue";
import { useAuthStore } from "@/stores/auth.js";
import { useAdminStore } from "@/stores/admin.js";
import router from "@/router";
import axios from "axios";

const auth = useAuthStore();
if (auth.token.type != "admin") {
	router.replace({path: "/"});
}

const admin = useAdminStore();

const is_loading = ref(true);
const style_cards = computed({
	get() {
		let dir = "column";
		if (admin.layout == "list") {
			dir = "row";
		}
		return {
			marginTop: "2em",
			display: "flex",
			flexDirection: dir,
		}
	}
})

function get_employees() {
	console.log("fetching employees...");
	is_loading.value = true;
	axios.get(
		`${CONST.API_URL}/employee/`,
		{headers: {"Authorization": `Bearer ${auth.token.access_token}`}}
	)
	.then(function(res) {
		is_loading.value = false;
		if (!res || res.status != 200)
			return
		admin.data = res.data.data;
	})
	.catch(function(error) {
		alert(error?.response?.data?.detail);
		is_loading.value = false;
	});
	console.log("done fetching employees");
}

get_employees();
</script>

<template>
	<h1>Admin View</h1>
	<Toolbar
		:fetch_employees=get_employees
	/>
	<div
		v-if="is_loading"
		class="card-container"
	>
	</div>
	<div
		v-else
		class="card-container"
		:style="style_cards"
	>
		<Card
			:id="idx"
			v-for="(emp, idx) in admin.data"
			:first_name="emp.first_name"
			:last_name="emp.last_name"
		/>
	</div>
</template>

<style scoped>
h1 {
	margin-top: 1em;
	margin-left: auto;
	margin-right: auto;
}
</style>
