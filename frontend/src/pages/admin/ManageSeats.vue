<template>
    <div class="container-fluid">
        <div class="row flex-nowrap">
            <main class="col py-4">
                <section class="card shadow-sm mb-4 p-4">
                    <h2 class="h5 fw-semibold mb-4">{{ $t('manageSeat') }}</h2>
                    <SeatManagement @seat-status-updated="handleSeatStatusUpdate" ref="seatManagement" />
                </section>
            </main>
        </div>
    </div>
</template>

<script>
import SeatManagement from '@/components/admin/SeatManagement.vue';

export default {
  components: {
    SeatManagement,
  },
  methods: {
    handleSeatStatusUpdate() {
      // You can extend this later to trigger global updates if needed
    },
  },
};
</script>
