<template>
  <div class="container">
    <h1 class="title">School Room Management</h1>
    <ul class="room-list">
      <li v-for="room in rooms" :key="room.id" class="room-item">
        <span class="room-name">{{ room.name }}</span> - Capacity: <span class="room-capacity">{{ room.capacity }}</span>
        <button @click="showReservations(room.id)">Show Reservations</button>
        <button @click="reserveRoom(room.id)">Reserve Room</button> <!-- Neuer Button für Reservierung -->
      </li>
    </ul>

    <div v-if="selectedRoom !== null">
      <h2>Reservations for {{ selectedRoom.name }}</h2>
      <ul>
        <li v-for="reservation in reservations" :key="reservation.room_id + reservation.user">
          {{ reservation.user }}
        </li>
      </ul>
      <input type="text" v-model="newReservationUser" placeholder="Enter your name">
      <button @click="reserveRoom(selectedRoom.id, newReservationUser)">Reserve Room</button> <!-- Neuer Button für Reservierung -->
    </div>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data() {
    return {
      rooms: [],
      reservations: [],
      selectedRoom: null,
      newReservationUser: ''
    }
  },
  mounted() {
    this.fetchRooms()
  },
  methods: {
    async fetchRooms() {
      try {
        const response = await fetch('http://localhost:8000/rooms');
        if (!response.ok) {
          throw new Error('Failed to fetch data');
        }
        this.rooms = await response.json();
      } catch (error) {
        console.error('Error:', error);
      }
    },
    async showReservations(roomId) {
      try {
        const response = await fetch(`http://localhost:8000/rooms/${roomId}/reservations`);
        if (!response.ok) {
          throw new Error('Failed to fetch reservations');
        }
        this.reservations = await response.json();
        this.selectedRoom = this.rooms.find(room => room.id === roomId);
      } catch (error) {
        console.error('Error:', error);
      }
    },
    async reserveRoom(roomId) {
      try {
        const user = prompt("Enter your name:");
        if (!user) return; // User canceled
        const response = await fetch(`http://localhost:8000/rooms/${roomId}/reserve`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ user })
        });
        if (!response.ok) {
          throw new Error('Failed to reserve room');
        }
        this.showReservations(roomId);
      } catch (error) {
        console.error('Error:', error);
      }
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.title {
  color: #42b983;
  font-size: 24px;
  margin-bottom: 20px;
}

.room-list {
  list-style-type: none;
  padding: 0;
}

.room-item {
  border-bottom: 1px solid #ccc;
  padding: 10px 0;
}

.room-name {
  font-weight: bold;
}

.room-capacity {
  color: #777;
}
</style>
