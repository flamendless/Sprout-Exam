import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import AdminView from "../views/AdminView.vue";
import EmployeeView from "../views/EmployeeView.vue";

const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: [
		{
			path: "/",
			name: "login",
			component: HomeView
		},
		{
			path: "/admin",
			name: "admin",
			component: AdminView
		},
		{
			path: "/employee/:employee_id",
			name: "employee",
			component: EmployeeView
		}
	]
});

export default router;
