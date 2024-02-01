<script setup>
import { ref } from "vue";
import { useAdminStore } from "@/stores/admin.js";

const admin = useAdminStore();

const input_email = ref("");
const input_password = ref("");
const input_password2 = ref("");
const input_first_name = ref("");
const input_last_name = ref("");
const input_type = ref("");
const input_number_of_leaves = ref(0);
const types = ["admin", "regular", "contractual"];

function handle_submit(e) {
	e.preventDefault();
	if (input_password.value != input_password2.value) {
		alert("Passwords must match");
	}

	const data = {
		email: input_email.value,
		password: input_password.value,
		first_name: input_first_name.value,
		last_name: input_last_name.value,
		type: input_type.value,
		number_of_leaves: input_number_of_leaves.value
	};
	admin.create_employee(data);
}
</script>

<template>
	<div class="form">
		<h1>Register Employee</h1>
		<form id="create_form" @submit.prevent="handle_submit">
			<div class="info">
				<div class="inputs">
					<label>
						<input type="text" v-model="input_email" placeholder="email" required />
					</label>

					<label>
						<input
							type="password"
							v-model="input_password"
							placeholder="password"
							required
						/>
					</label>

					<label>
						<input
							type="password"
							v-model="input_password2"
							placeholder="confirm password"
							required
						/>
					</label>

					<label>
						<input
							type="text"
							v-model="input_first_name"
							placeholder="first name"
							required
						/>
					</label>

					<label>
						<input
							type="text"
							v-model="input_last_name"
							placeholder="last name"
							required
						/>
					</label>

					<label for="type-choice">
						<input list="type-choices" v-model="input_type" required />
					</label>
					<datalist id="type-choices">
						<option v-for="type in types" :value="type">
							{{ type }}
						</option>
					</datalist>

					<label>
						<input
							type="number"
							v-model="input_number_of_leaves"
							placeholder="number of leaves"
							required
						/>
					</label>
				</div>

				<div class="labels">
					<label>email</label>
					<label>password</label>
					<label>confirm password</label>
					<label>first name</label>
					<label>last name</label>
					<label>type</label>
					<label>number of leaves</label>
				</div>
			</div>

			<div class="buttons">
				<button @click="admin.toggle_create_form">
					<span class="pi pi-times"></span>
				</button>

				<button type="submit">
					<span class="pi pi-check"></span>
				</button>
			</div>
		</form>
	</div>
</template>

<style scoped>
.form {
	border-style: solid;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: space-evenly;
	flex-grow: 1;
}

.form h1 {
	margin: 1em;
}

.form form {
	display: flex;
	flex-grow: 1;
	flex-direction: column;
	align-items: center;
	margin: 2em;
	width: 100%;
}

.form form .info {
	display: flex;
	flex-direction: row;
	flex-grow: 1;
	align-items: center;
	width: 100%;
}

.form form .info .inputs {
	display: flex;
	flex-direction: column;
	width: 100%;
	align-items: flex-end;
}

.form form .info .labels {
	display: flex;
	flex-direction: column;
	width: 100%;
	align-items: flex-start;
}

.form form label {
	padding: 0.75em;
}

.form form .buttons {
	display: flex;
	flex-grow: 1;
	flex-direction: row;
	justify-content: space-between;
	margin: 2em;
	width: 30%;
}

.form form .buttons button {
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

.form form .buttons button:hover {
	cursor: pointer;
}
</style>