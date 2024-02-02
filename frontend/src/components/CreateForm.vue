<script setup>
import { ref, onMounted, computed } from "vue";
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
const input_contract_end_date = ref("");

const benefits = computed({
	get() {
		return admin.benefits;
	}
});
const input_benefit = ref("");

const projects = computed({
	get() {
		return admin.projects;
	}
});
const input_project = ref("");

function handle_submit(e) {
	e.preventDefault();
	if (input_password.value != input_password2.value) {
		alert("Passwords must match");
		return;
	}

	const data = {
		email: input_email.value,
		password: input_password.value,
		first_name: input_first_name.value,
		last_name: input_last_name.value,
		type: input_type.value,
		number_of_leaves: input_number_of_leaves.value,
		contract_end_date: input_contract_end_date.value
	};
	admin.create_employee(data, input_benefit.value, input_project.value);
}

onMounted(function () {
	admin.get_benefits();
	admin.get_projects();
});
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

					<label v-if="input_type == 'admin' || input_type == 'regular'">
						<input
							type="number"
							v-model="input_number_of_leaves"
							placeholder="number of leaves"
							required
						/>
					</label>

					<label v-if="input_type == 'contractual'">
						<input
							type="datetime-local"
							v-model="input_contract_end_date"
							placeholder="contract end date"
							:required="input_type == 'contractual'"
						/>
					</label>

					<label
						for="benefit-choice"
						v-if="input_type == 'regular' || input_type == 'admin'"
					>
						<input
							list="benefit-choices"
							v-model="input_benefit"
							:required="input_type == 'regular'"
						/>
					</label>
					<datalist
						id="benefit-choices"
						v-if="input_type == 'regular' || input_type == 'admin'"
					>
						<option v-for="benefit in benefits" :value="benefit.name">
							{{ benefit.name }}
						</option>
					</datalist>

					<label
						for="project-choice"
						v-if="input_type == 'contractual' || input_type == 'admin'"
					>
						<input
							list="project-choices"
							v-model="input_project"
							:required="input_type == 'contractual'"
						/>
					</label>
					<datalist
						id="project-choices"
						v-if="input_type == 'contractual' || input_type == 'admin'"
					>
						<option v-for="project in projects" :value="project.name">
							{{ project.name }}
						</option>
					</datalist>
				</div>

				<div class="labels">
					<label>email</label>
					<label>password</label>
					<label>confirm password</label>
					<label>first name</label>
					<label>last name</label>
					<label>type</label>
					<label v-if="input_type == 'admin' || input_type == 'regular'"
						>number of leaves</label
					>
					<label v-if="input_type == 'contractual'">contract end date</label>
					<label v-if="input_type == 'regular' || input_type == 'admin'">benefit</label>
					<label v-if="input_type == 'contractual' || input_type == 'admin'"
						>project</label
					>
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
