import { defineStore } from "pinia";
import axios from "axios";
import router from "@/router";
import CONST from "@/const.js";

export const useAuthStore = defineStore("auth", {
	persist: true,

	state: () => {
		return {
			token: {
				access_token: "",
				expires_in: "",
				refresh_token: "",
				token_type: "",
				type: ""
			},
			err_message: ""
		};
	},

	actions: {
		login(form_data) {
			const auth = this;
			axios
				.post(`${CONST.API_URL}/auth/token`, form_data)
				.then(function (res) {
					if (!res || res.status != 200) return;

					auth.token.access_token = res.data.access_token;
					auth.token.expires_in = res.data.expires_in;
					auth.token.refresh_token = res.data.refresh_token;
					auth.token.token_type = res.data.token_type;
					auth.token.type = res.data.type;
					if (auth.token.type == "admin") {
						router.replace({ path: "/admin" });
					}
				})
				.catch(function (error) {
					auth.err_message = error.response.data.detail;
				});
		},
		logout() {
			console.log(111);
			this.$reset();
			router.replace({ path: "/" });
		}
	}
});
