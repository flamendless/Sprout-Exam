<script setup>
import { ref } from "vue";
import router from "@/router";
import { useAuthStore } from "@/stores/auth.js";
import CONST from "@/const.js";
console.log(CONST.API_URL)

const auth = useAuthStore();
if (auth.token.type == "admin") {
	router.push({ path: "/admin/" });
}

const input_username = ref("");
const input_password = ref("");

function handle_submit(e) {
	e.preventDefault();
	const form_data = new FormData();
	form_data.append("username", input_username.value);
	form_data.append("password", input_password.value);
	auth.login(form_data);
}
</script>

<template>
	<div class="login">
		<h1 class="green">Sprout Employee Solutions</h1>
		<div class="box">
			<form @submit.prevent="handle_submit">
				<label>
					<input type="text" v-model="input_username" placeholder="username" required />
					username
				</label>

				<label>
					<input
						type="password"
						v-model="input_password"
						placeholder="password"
						required
					/>
					password
				</label>

				<h3 class="error" v-if="auth.err_message != ''">
					{{ auth.err_message }}
				</h3>

				<button type="submit">LOG IN</button>
			</form>
		</div>
	</div>
</template>

<style scoped>
.login {
	margin-top: 2em;
	align-self: center;
	padding: 4em;
	border-style: solid;
	display: flex;
	flex-direction: column;
	align-items: center;
}

.login h1 {
	margin-bottom: 2em;
}

.box {
	border-style: solid;
	padding: 4em;
}

form {
	display: flex;
	flex-direction: column;
	align-items: center;
}

label {
	display: block;
	margin: 2em;
}

label:hover {
	border-radius: 6px;
	cursor: pointer;
	background-color: rgb(200, 200, 200);
}

button {
	margin-top: 2em;
}

.error {
	color: red;
}
</style>
