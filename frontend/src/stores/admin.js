import { defineStore } from "pinia";
import { useAuthStore } from "@/stores/auth.js";
import axios from "axios";
import router from "@/router";
import CONST from "@/const.js";
import { EmployeeType } from "@/enums.js";

export const useAdminStore = defineStore("admin", {
	state: () => ({
		data: [],
		is_loading: true,
		layout: "grid",

		show_create_form: false,
		show_edit_form: false,

		edit_id: -1,

		//here maps should be used for O(1) access
		//but Pinia dislikes map in states
		employees: [],
		benefits: [],
		projects: []
	}),

	actions: {
		toggle_layout() {
			if (this.layout == "grid") {
				this.layout = "list";
			} else if (this.layout == "list") {
				this.layout = "grid";
			}
		},

		toggle_create_form() {
			this.show_edit_form = false;
			this.edit_id = -1;
			this.show_create_form = !this.show_create_form;
		},

		toggle_edit_form(employee_id) {
			this.show_create_form = false;
			if (employee_id == -1) {
				this.show_edit_form = false;
				this.edit_id = employee_id;
				return;
			}

			if (this.edit_id == -1) this.show_edit_form = true;
			else this.show_edit_form = employee_id != this.edit_id;
			this.edit_id = employee_id;
		},

		get_employee_by_id(employee_id) {
			const auth = useAuthStore();
			const admin = this;
			axios
				.get(`${CONST.API_URL}/employee/${employee_id}`, {
					headers: { Authorization: `Bearer ${auth.token.access_token}` }
				})
				.then(function (res) {
					if (!res || res.status != 200) return;
					admin.employees[res.data.id] = res.data;
				})
				.catch(function (error) {
					alert(error?.response?.data?.detail);
				});
		},

		get_employees() {
			const auth = useAuthStore();
			console.log("fetching employees...");
			const admin = this;
			admin.is_loading = true;
			axios
				.get(`${CONST.API_URL}/employee/`, {
					headers: { Authorization: `Bearer ${auth.token.access_token}` }
				})
				.then(function (res) {
					admin.is_loading = false;
					if (!res || res.status != 200) return;
					admin.data = res.data.data;
				})
				.catch(function (error) {
					alert(error?.response?.data?.detail);
					admin.is_loading = false;
				});
			console.log("done fetching employees");
		},

		create_employee(data, benefit_name, project_name) {
			const auth = useAuthStore();
			const admin = this;
			axios
				.post(`${CONST.API_URL}/employee/`, data, {
					headers: { Authorization: `Bearer ${auth.token.access_token}` }
				})
				.then(function (res) {
					if (!res || res.status != 200) return;

					if (data.type == EmployeeType.REGULAR || data.type == EmployeeType.ADMIN) {
						admin.assign_employee_to_benefit(res.data.id, benefit_name);
					}

					if (data.type == EmployeeType.CONTRACTUAL || data.type == EmployeeType.ADMIN) {
						admin.assign_employee_to_project(res.data.id, project_name);
					}

					admin.toggle_create_form();
					admin.get_employees();
					alert("Successfully registered new employee");
				})
				.catch(function (error) {
					const msg = error.response?.data?.message;
					if (msg) {
						alert(msg);
						return;
					}

					const details = error.response.data.detail;
					let err = "";
					for (let i = 0; i < details.length; i++) {
						const detail = details[i];
						err += `${detail.loc[1]} - ${detail.msg}\n`;
					}
					alert(err);
				});
		},

		update_employee(employee_id, data) {
			const auth = useAuthStore();
			const admin = this;
			axios
				.patch(`${CONST.API_URL}/employee/${employee_id}`, data, {
					headers: { Authorization: `Bearer ${auth.token.access_token}` }
				})
				.then(function (res) {
					if (!res || res.status != 200) return;
					admin.get_employee_by_id(admin.edit_id);
					admin.get_employees();
					admin.toggle_edit_form(-1);
					alert("Successfully updated employee");
				})
				.catch(function (error) {
					const msg = error.response.data?.message;
					if (msg) {
						alert(msg);
						return;
					}

					const details = error.response.data.detail;
					let err = "";
					for (let i = 0; i < details.length; i++) {
						const detail = details[i];
						err += `${detail.loc[1]} - ${detail.msg}\n`;
					}
					alert(err);
				});
		},

		delete_employee(employee_id) {
			const sure = confirm("Are you sure you want to delete this employee?");
			if (sure === false) return;
			const auth = useAuthStore();
			const admin = this;
			axios
				.delete(`${CONST.API_URL}/employee/${employee_id}`, {
					headers: { Authorization: `Bearer ${auth.token.access_token}` }
				})
				.then(function (res) {
					if (!res || res.status != 200) return;
					admin.get_employees();
				})
				.catch(function (error) {
					alert(error.response.data);
				});
		},

		get_benefits() {
			const auth = useAuthStore();
			console.log("fetching benefits...");
			const admin = this;
			axios
				.get(`${CONST.API_URL}/benefit/`, {
					headers: { Authorization: `Bearer ${auth.token.access_token}` }
				})
				.then(function (res) {
					if (!res || res.status != 200) return;
					admin.benefits = res.data.data;
				})
				.catch(function (error) {
					alert(error?.response?.data?.detail);
				});
			console.log("done fetching benefits");
		},

		get_projects() {
			const auth = useAuthStore();
			console.log("fetching projects...");
			const admin = this;
			axios
				.get(`${CONST.API_URL}/project/`, {
					headers: { Authorization: `Bearer ${auth.token.access_token}` }
				})
				.then(function (res) {
					if (!res || res.status != 200) return;
					admin.projects = res.data.data;
				})
				.catch(function (error) {
					alert(error?.response?.data?.detail);
				});
			console.log("done fetching projects");
		},

		assign_employee_to_benefit(employee_id, benefit_name) {
			const admin = this;

			let benefit_id = -1;
			for (let i = 0; i < admin.benefits.length; i++) {
				const benefit = admin.benefits[i];
				if (benefit.name == benefit_name) {
					benefit_id = benefit.id;
					break;
				}
			}

			const auth = useAuthStore();
			axios
				.post(`${CONST.API_URL}/benefit/${benefit_id}/assign`, [employee_id], {
					headers: { Authorization: `Bearer ${auth.token.access_token}` }
				})
				.then(function (res) {
					if (!res || res.status != 200) return;
				})
				.catch(function (error) {
					alert(error?.response?.data?.detail);
				});
		},

		assign_employee_to_project(employee_id, project_name) {
			const admin = this;

			let project_id = -1;
			for (let i = 0; i < admin.projects.length; i++) {
				const project = admin.projects[i];
				if (project.name == project_name) {
					project_id = project.id;
					break;
				}
			}

			const auth = useAuthStore();
			axios
				.post(`${CONST.API_URL}/project/${project_id}/assign`, [employee_id], {
					headers: { Authorization: `Bearer ${auth.token.access_token}` }
				})
				.then(function (res) {
					if (!res || res.status != 200) return;
				})
				.catch(function (error) {
					alert(error?.response?.data?.detail);
				});
		}
	}
});
