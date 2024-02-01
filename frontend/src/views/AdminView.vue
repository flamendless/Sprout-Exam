<script setup>
import { computed } from "vue";
import Card from "@/components/Card.vue";
import Toolbar from "@/components/Toolbar.vue";
import CreateForm from "@/components/CreateForm.vue";
import { useAuthStore } from "@/stores/auth.js";
import { useAdminStore } from "@/stores/admin.js";
import router from "@/router";
import { onMounted } from "vue";

const auth = useAuthStore();
if (auth.token.type != "admin") {
	router.replace({ path: "/" });
}

const admin = useAdminStore();
onMounted(function () {
	admin.get_employees();
});

const style_cards = computed({
	get() {
		let dir;
		if (admin.layout == "list") {
			dir = "column";
		} else if (admin.layout == "grid") {
			dir = "row";
		}
		return {
			marginTop: "2em",
			display: "flex",
			flexDirection: dir,
			flexWrap: "wrap"
		};
	}
});
</script>

<template>
	<h1>Admin View</h1>
	<Toolbar />
	<CreateForm v-if="admin.show_create_form" />
	<div v-if="admin.is_loading" class="card-container"></div>
	<div v-else class="card-container" :style="style_cards">
		<Card
			:id="idx"
			v-for="(emp, idx) in admin.data"
			:employee_id="emp.id"
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
