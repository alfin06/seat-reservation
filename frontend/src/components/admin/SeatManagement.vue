<template>
    <div class="seat-management">
      <div class="action-bar">
        <!-- <el-button type="primary" @click="showDialog('add')">
          <i class="el-icon-plus"></i> Add Seat
        </el-button> -->
        <el-input
          v-model="searchQuery"
          placeholder="Search seat..."
          clearable
          style="width: 300px; margin-left: 10px;"
        />
      </div>
  
      <el-table :data="displayedSeats" border>
        <!-- Name -->
        <el-table-column prop="name" label="Seat Name" sortable />
  
        <!-- Location -->
        <el-table-column prop="location" label="Location" />

        <el-table-column prop="classroom" label="Classroom" />
  
        <!-- Availability -->
        <el-table-column label="Available" width="120">
          <template #default="{ row }">
            <el-tag :type="row.is_available.value ? 'success' : 'warning'">
              {{ row.is_available.display }}
            </el-tag>
          </template>
        </el-table-column>
  
        <!-- Disabled -->
        <el-table-column label="Status" width="120">
          <template #default="{ row }">
            <el-tag :type="row.is_disable.value ? 'danger' : 'info'">
              {{ row.is_disable.display }}
            </el-tag>
          </template>
        </el-table-column>
  
        <!-- Updated At -->
        <el-table-column prop="updated_at" label="Last Updated" width="180" />
  
        <!-- Actions -->
        <el-table-column label="Actions" width="200">
          <template #default="{ row }">
            <el-button
              size="mini"
              @click="showDialog('edit', row)"
            >
              Edit
              <i class="el-icon-edit" style="margin-left:4px;"></i>
            </el-button>
            <!-- <el-button
              type="warning"
              size="mini"
              icon="el-icon-switch-button"
              @click="toggleDisable(row)"
            /> -->
            <el-button
              type="danger"
              size="mini"
              @click="toggleDisable (row)"
              >
              Disable
            </el-button>
          </template>
        </el-table-column>
      </el-table>
  
      <!-- Add / Edit Dialog -->
      <el-dialog
        :title="dialogTitle"
        :visible.sync="dialogVisible"
        width="40%"
      >
        <el-form :model="currentSeat" label-width="120px">
          <el-form-item label="Seat Name" required>
            <el-input v-model="currentSeat.name" />
          </el-form-item>
          <el-form-item label="Location">
            <el-input v-model="currentSeat.location" />
          </el-form-item>
          <el-form-item label="Available">
            <el-switch
              v-model="currentSeat.is_available.value"
              active-text="Available"
              inactive-text="Reserved"
            />
          </el-form-item>
          <el-form-item label="Disabled">
            <el-switch
              v-model="currentSeat.is_disable.value"
              active-text="Disabled"
              inactive-text="Active"
            />
          </el-form-item>
        </el-form>
        <span slot="footer">
          <el-button @click="dialogVisible = false">Cancel</el-button>
          <el-button type="primary" @click="saveSeat">Save</el-button>
        </span>
      </el-dialog>

      <!-- Pagination Controls -->
      <div class="pagination">
        <el-pagination
          background
          layout="prev, pager, next"
          :current-page="currentPage"
          :page-size="pageSize"
          :total="filteredSeats.length"
          @current-change="handlePageChange"
        />
      </div>
    </div>
</template>
  
  <script>
  import axios from 'axios'
  
  export default {
    data() {
      return {
        currentPage: 1,
        pageSize: 15,
        seats: [],
        searchQuery: '',
        dialogVisible: false,
        dialogMode: 'add',
        currentSeat: this.getDefaultSeat(),
      }
    },
    computed: {
      filteredSeats() {
        return this.seats.filter(r =>
          r.name.toLowerCase().includes(this.searchQuery.toLowerCase())
        )
      },
      displayedSeats() {
        const start = (this.currentPage - 1) * this.pageSize
        const end = start + this.pageSize
        return this.filteredSeats.slice(start, end)
      },
      totalPages() {
        return Math.ceil(this.filteredSeats.length / this.pageSize)
      },
      dialogTitle() {
        return this.dialogMode === 'add' ? 'Add New Seat' : 'Edit Seat'
      }
    },
    methods: {
      handlePageChange(newPage) {
        this.currentPage = newPage
      },

      getDefaultSeat() {
        return {
          id: null,
          name: '',
          location: '',
          classroom: '',
          is_available: { value: 1, display: 'Available' },
          is_disable:   { value: 0, display: 'Active' },
          updated_at: ''
        }
      },
  
      async fetchSeats() {
        try {
          const res = await axios.get('http://127.0.0.1:8000/dashboard/admin/seats/list/')
          if (res.data.status === 'success') {
            this.seats = res.data.data.map((c, i) => ({
              id: c.id,
              name: 'Seat ' + c.id + '-' + c.location,
              location: c.location,
              classroom: c.classroom,
              is_available: c.is_available,
              is_disable: c.is_disable, 
              updated_at: c.update_at
            }))
          } else {
            this.$message.error(res.data.message || 'Failed to load seats')
          }
        } catch (err) {
          console.error(err)
          this.$message.error('Server error fetching seats')
        }
      },
  
      showDialog(mode, seat = null) {
        this.dialogMode = mode
        this.currentSeat = seat
          ? JSON.parse(JSON.stringify(seat))
          : this.getDefaultSeat()
        this.dialogVisible = true
      },
  
      async saveSeat() {
        // stub: wire up to your create/update API as needed
        this.dialogVisible = false
        await this.fetchSeats()
      },
  
      async toggleDisable(row) {
        // stub: call your disable API
        try {
          const payload = { id: row.id };
          console.log('Disable room id: ' + row.id);
          const res = await axios.post(
            'http://127.0.0.1:8000/dashboard/admin/seats/disable/',
            payload,
            { headers: { 'Content-Type': 'application/json' } }
          );

          if (res.data.status === 'success') {
            this.$message.success('Seat status toggled.');
          } else {
            this.$message.error(res.data.message || 'Failed to toggle seat.');
          }
          
          // refresh list
          await this.fetchSeats();
        } catch (err) {
          console.error(err);
          this.$message.error('Server error toggling seat. Disable room id: ' + row.id);
        }
      },
  
      async deleteSeat(row) {
        // stub: call your delete API
        await this.fetchSeats()
      },
      searchQuery() {
        this.currentPage = 1 
      }
    },
    watch: {
      searchQuery() {
        this.currentPage = 1
      }
   },
    mounted() {
      this.fetchSeats()
    }
  }
  </script>
  
  <style scoped>
  .action-bar {
    display: flex;
    margin-bottom: 20px;
    align-items: center;
  }
  </style>
  