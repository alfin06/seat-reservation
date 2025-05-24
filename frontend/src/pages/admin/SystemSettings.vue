<template>
    <div class="container-fluid">
        <div class="row flex-nowrap">
            <main class="col py-4">
                <section class="card shadow-sm mb-4 p-4">
                    <h2 class="h5 fw-semibold mb-4">{{ $t('settings') }}</h2>
                    <SystemSettings />
                </section>
                <section class="card shadow-sm mb-4 p-4">
                    <h2 class="h5 fw-semibold mb-4">{{ $t('userManagement') }}</h2>
                    <UserManagement />
                </section>
            </main>
        </div>
    </div>
</template>

<script>
import SystemSettings from '@/components/admin/SystemSettings.vue';
import UserManagement from '@/components/admin/UserManagement.vue';

export default {
  components: {
    SystemSettings,
    UserManagement
  },
};
</script>
