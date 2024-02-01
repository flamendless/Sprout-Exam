<script setup>
import { ref } from "vue";
import CONST from "@/const.js";
import axios from "axios";
import router from "@/router";
import { useTokenStore } from "@/stores/token";

const token = useTokenStore();
if (token.type == "admin") {
	router.replace({path: "/admin"});
}

const input_username = ref("");
const input_password = ref("");
const err_message = ref("");

async function handle_submit(e) {
	e.preventDefault();
	const data = new FormData();
	data.append("username", input_username.value);
	data.append("password", input_password.value);

	axios
		.post(`${CONST.API_URL}/auth/token`, data)
		.then((res) => {
			if (res && res.status == 200) {
				token.access_token = res.data.access_token;
				token.expires_in = res.data.expires_in;
				token.refresh_token = res.data.refresh_token;
				token.token_type = res.data.token_type;
				token.type = res.data.type;

				if (token.type == "admin") {
					router.replace({path: "/admin"});
				}
			}
		})
		.catch((error) => {
			err_message.value = error.response.data.detail;
		});
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

				<h3 class="error" v-if="err_message != ''">
					{{ err_message }}
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
