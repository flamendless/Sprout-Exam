<script setup>
import { useAuthStore } from "@/stores/auth.js";
import { useRoute } from "vue-router";
import router from "@/router";

const auth = useAuthStore();
if (auth.token.type != "admin") {
	router.replace({ path: "/" });
}

const route = useRoute();
const employee_id = route.params.employee_id;
if (employee_id == null || employee_id == undefined) {
	router.replace({ path: "/admin" });
}
</script>

<template>
	<h1>Employee View</h1>
</template>

<style scoped>
h1 {
	margin-top: 1em;
	margin-left: auto;
	margin-right: auto;
}
</style>
