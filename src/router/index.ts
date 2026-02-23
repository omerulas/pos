import { useProcess } from "@/stores/process";
import Workspace from "@/views/layers/Workspace.vue";
import Main from "@/views/private/Main.vue";
import Home from "@/views/public/Home.vue";
import Login from "@/views/public/Login.vue";
import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "",
      children: [
        {
          path: "",
          name: "home",
          component: Home,
        },
        {
          path: "login",
          name: "login",
          component: Login,
          meta: { requiresGuest: true },
        },
      ],
    },
    {
      path: "/workspace",
      meta: { requiresAuth: true },
      component: Workspace,
      children: [
        {
          path: "",
          name: "workspace",
          component: Main,
        },
        {
          path: "table/:id",
          name: "table",
          component: () => import("@/views/private/Table.vue"),
        },
      ],
    },
  ],
});

router.beforeEach(async (to, from) => {
  const process = useProcess();
  if (!process.isChecked) {
    await process.check();
  }

  const requiresAuth = to.matched.some((record) => {
    return record.meta.requiresAuth;
  });

  const requiresGuest = to.matched.some((record) => {
    return record.meta.requiresGuest;
  });

  if (requiresAuth && !process.isAuthenticated) {
    return { name: "login", query: { redirect: to.fullPath } };
  }

  if (requiresGuest && process.isAuthenticated) {
    return { name: "workspace" };
  }
});

export default router;
