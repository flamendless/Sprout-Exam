<script setup>
import { useTokenStore } from "@/stores/token";
import router from "@/router";

const token = useTokenStore();
if (token.type != "admin") {
	router.replace({path: "/"});
}
</script>

<template>
	<h1>Hi</h1>
</template>
