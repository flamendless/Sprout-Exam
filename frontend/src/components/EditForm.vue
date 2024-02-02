<script setup>
import { computed, ref } from "vue";
import { useAdminStore } from "@/stores/admin.js";

const admin = useAdminStore();

const input_email = ref("");
const input_current_password = ref("");
const input_new_password = ref("");
const input_first_name = ref("");
const input_last_name = ref("");
const input_type = ref("");
const input_number_of_leaves = ref(0);
const types = ["admin", "regular", "contractual"];
const input_contract_end_date = ref("");

const employee_data = computed({
	get() {
		for (let i = 0; i < admin.data.length; i++) {
			if (admin.data[i].id == admin.edit_id) {
				const d = admin.data[i];
				input_email.value = d.email;
				input_first_name.value = d.first_name;
				input_last_name.value = d.last_name;
				input_type.value = d.type;
				input_number_of_leaves.value = d.number_of_leaves;
				input_contract_end_date.value = d.contract_end_date;
				return d
			}
		}
		return {}
	}
});

function handle_submit(e) {
	e.preventDefault();

	if (input_new_password.value && !input_current_password.value) {
		alert("Current password is needed when changing password");
		return;
	}

	if (
		input_current_password.value &&
		input_new_password.value &&
		input_current_password.value == input_new_password.value
	) {
		alert("New password must not be the same as the current password");
		return;
	}

	const data = {
		email: input_email.value,
		password: input_new_password.value,
		first_name: input_first_name.value,
		last_name: input_last_name.value,
		type: input_type.value,
		number_of_leaves: input_number_of_leaves.value,
		contract_end_date: input_contract_end_date.value,
	};

	Object.keys(data).forEach((key) => {
		if (data[key] == null || data[key] == "") {
			delete data[key];
		}
	});

	admin.update_employee(admin.edit_id, data);
}
</script>

<template>
	<div class="form">
		<h1>Edit Employee {{admin.edit_id}}</h1>
		<form id="create_form" @submit.prevent="handle_submit">
			<div class="info">
				<div class="inputs">
					<label>
						<input
							type="text"
							v-model="input_email"
							:placeholder="employee_data.email"
							required
						/>
					</label>

					<label>
						<input
							type="password"
							v-model="input_current_password"
							placeholder="current password"
						/>
					</label>

					<label>
						<input
							type="password"
							v-model="input_new_password"
							placeholder="new password"
						/>
					</label>

					<label>
						<input
							type="text"
							v-model="input_first_name"
							:placeholder="employee_data.first_name"
							required
						/>
					</label>

					<label>
						<input
							type="text"
							v-model="input_last_name"
							:placeholder="employee_data.last_name"
							required
						/>
					</label>

					<label for="type-choice">
						<input
							list="type-choices"
							v-model="input_type"
							:placeholder="employee_data.type"
							required
						/>
					</label>
					<datalist id="type-choices">
						<option v-for="type in types" :value="type">
							{{ type }}
						</option>
					</datalist>

					<label v-if="employee_data.type == 'admin' || employee_data.type == 'regular'">
						<input
							type="number"
							v-model="input_number_of_leaves"
							:placeholder="employee_data.number_of_leaves"
							required
						/>
					</label>

					<label v-if="employee_data.type == 'contractual'">
						<input
							type="datetime-local"
							v-model="input_contract_end_date"
							placeholder="contract end date"
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
					<label v-if="employee_data.type == 'admin' || employee_data.type == 'regular'">
						number of leaves
					</label>
					<label v-if="employee_data.type == 'contractual'">contract end date</label>
				</div>
			</div>

			<div class="buttons">
				<button @click="admin.toggle_edit_form(-1)">
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
	width: 50%;
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
