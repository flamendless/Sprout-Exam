<script setup>
import { RouterView } from "vue-router";
</script>

<template>
	<header>
		<img
			alt="Sprout logo"
			class="logo"
			src="@/assets/sprout_logo.png"
			width="256"
			height="125"
		/>
	</header>

	<RouterView />
</template>

<style scoped>
header {
	padding-top: 2rem;
	line-height: 1.5;
	max-height: 100vh;
	display: flex;
	flex-direction: column;
	align-items: center;
}

.logo {
	display: block;
}

nav {
	width: 100%;
	font-size: 12px;
	text-align: center;
	margin-top: 2rem;
}

nav a.router-link-exact-active {
	color: var(--color-text);
}

nav a.router-link-exact-active:hover {
	background-color: transparent;
}

nav a {
	display: inline-block;
	padding: 0 1rem;
	border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
	border: 0;
}

@media (min-width: 1024px) {
	header {
		display: flex;
		place-items: center;
	}

	header .wrapper {
		display: flex;
		place-items: flex-start;
		flex-wrap: wrap;
		flex-grow: 1;
	}

	nav {
		text-align: left;
		margin-left: -1rem;
		font-size: 1rem;

		padding: 1rem 0;
		margin-top: 1rem;
	}
}
</style>
