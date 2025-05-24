<template>
    <div class="container-fluid">
        <div class="row flex-nowrap">
            <main class="col py-4">
                <section class="card shadow-sm mb-4 p-4">
                    <h2 class="h5 fw-semibold mb-4">{{ $t('manageRoom') }}</h2>
                    <RoomManagement @room-status-updated="handleRoomStatusUpdate" />
                </section>
            </main>
        </div>
  </div>
</template>

<script>
import RoomManagement from '@/components/admin/RoomManagement.vue';

export default {
  components: {
    RoomManagement,
  },
  methods: {
    handleRoomStatusUpdate() {
      // Placeholder if needed for callback
    },
  },
};
</script>
