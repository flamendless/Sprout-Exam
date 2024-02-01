import { defineStore } from "pinia";
import { useAuthStore } from "@/stores/auth.js";
import axios from "axios";
import router from "@/router";
import CONST from "@/const.js";

export const useAdminStore = defineStore("admin", {
	state: () => ({
		data: [],
		show_create_form: false,
		is_loading: true,
		layout: "grid"
	}),

	actions: {
		toggle_layout() {
			if (this.layout == "grid") {
				this.layout = "list";
			} else if (this.layout == "list") {
				this.layout = "grid";
			}
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
					if (!res || res.status != 200)
						return;
					admin.data = res.data.data;
				})
				.catch(function (error) {
					alert(error?.response?.data?.detail);
					admin.is_loading = false;
				});
			console.log("done fetching employees");
		},

		toggle_create_form() {
			this.show_create_form = !this.show_create_form;
		},

		create_employee(data) {
			const auth = useAuthStore();
			const admin = this;
			axios
				.post(`${CONST.API_URL}/employee/`, data, {
					headers: { Authorization: `Bearer ${auth.token.access_token}` }
				})
				.then(function (res) {
					if (!res || res.status != 200) return;
					admin.toggle_create_form();
					admin.get_employees();
					alert("Successfully registered new employee");
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
		}
	}
});
