<script setup>
import { computed } from "vue";
import { useAuthStore } from "@/stores/auth.js";
import { useAdminStore } from "@/stores/admin.js";
import { useRoute } from "vue-router";
import { onMounted } from "vue";
import EditForm from "@/components/EditForm.vue";
import router from "@/router";
import { EmployeeType } from "@/enums.js";

const auth = useAuthStore();
if (auth.token.type != EmployeeType.ADMIN) {
	router.push({ path: "/" });
}

const route = useRoute();
const employee_id = route.params.employee_id;
if (employee_id == null || employee_id == undefined) {
	router.push({ path: "/admin/" });
}

const admin = useAdminStore();
const employee_data = computed({
	get() {
		if (admin.employees.length > employee_id) {
			return admin.employees[employee_id];
		}
		return null;
	}
});

function go_back() {
	router.push({ path: "/admin/" });
}

onMounted(function () {
	admin.get_employee_by_id(employee_id);
	admin.show_edit_form = false;
	admin.edit_id = -1;
});
</script>

<template>
	<h1>Employee View</h1>
	<EditForm v-if="admin.show_edit_form" />
	<div class="box" v-else>
		<div v-if="employee_data" class="data">
			<span class="pi pi-user user"></span>
			<div class="parent">
				<div class="left">
					<h3>Name</h3>
					<h3>E-Mail</h3>
					<h3>Type</h3>

					<h3 v-if="employee_data.type == 'regular' || employee_data.type == 'admin'">
						Number of Leaves
					</h3>
					<h3 v-if="employee_data.type == 'contractual' || employee_data.type == 'admin'">
						Contract End Date
					</h3>
					<h3
						v-if="employee_data.type == 'regular' || employee_data.type == 'admin'"
						v-for="(_, idx) in employee_data.benefits"
					>
						Benefit #{{ idx + 1 }}
					</h3>
					<h3
						v-if="employee_data.type == 'contractual' || employee_data.type == 'admin'"
						v-for="(_, idx) in employee_data.projects"
					>
						Project #{{ idx + 1 }}
					</h3>
				</div>
				<div class="right">
					<h3>{{ employee_data.first_name }} {{ employee_data.last_name }}</h3>
					<h3>{{ employee_data.email }}</h3>
					<h3>{{ employee_data.type }}</h3>

					<h3 v-if="employee_data.type == 'regular' || employee_data.type == 'admin'">
						{{ employee_data.number_of_leaves || 0 }}
					</h3>
					<h3 v-if="employee_data.type == 'contractual' || employee_data.type == 'admin'">
						{{ employee_data.contract_end_date }}
					</h3>
					<h3
						v-if="employee_data.type == 'regular' || employee_data.type == 'admin'"
						v-for="benefit in employee_data.benefits"
					>
						{{ benefit.name }}
					</h3>
					<h3
						v-if="employee_data.type == 'contractual' || employee_data.type == 'admin'"
						v-for="project in employee_data.projects"
					>
						{{ project.name }}
					</h3>
				</div>
			</div>

			<div class="buttons">
				<button @click="go_back">
					<span class="pi pi-arrow-left"></span>
				</button>
				<button @click="admin.toggle_edit_form(employee_id)">
					<span class="pi pi-user-edit"></span>
				</button>
				<button @click="admin.delete_employee(employee_id)">
					<span class="pi pi-trash"></span>
				</button>
			</div>
		</div>
	</div>
</template>

<style scoped>
h1 {
	margin-top: 1em;
	margin-left: auto;
	margin-right: auto;
	margin-bottom: 1em;
}

.buttons {
	display: flex;
	flex-direction: row;
	align-items: center;
	justify-content: space-evenly;
	width: 100%;
}

.buttons button {
	margin-top: 2em;
	background-color: transparent;
	padding-left: 1.5em;
	padding-right: 1.5em;
	padding-top: 0.5em;
	padding-bottom: 0.5em;
	color: hsla(160, 100%, 37%, 1);
}

.user {
	font-size: 4em;
	margin-bottom: 1rem;
}

.box {
	border-style: solid;
	padding: 4em;
	display: flex;
	flex-direction: column;
	align-items: center;
}

.data {
	display: flex;
	flex-direction: column;
	align-items: center;
}

.parent {
	display: flex;
	flex-direction: row;
	flex-grow: 1;
}

.left {
	align-self: flex-end;
	margin: 1em;
	text-align: right;
}

.right {
	align-self: flex-start;
	margin: 1em;
}
</style>
