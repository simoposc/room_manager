<template>
  <div class="container">
    <h1 class="title">School Room Management</h1>
    <ul class="room-list">
      <li v-for="room in rooms" :key="room.id" class="room-item">
        <span class="room-name">{{ room.name }}</span> - 
        <button @click="showReservations(room.id)">Show Reservations</button>
      </li>
    </ul>

    <div v-if="selectedRoom !== null">
      <h2>Reservations for {{ selectedRoom.name }}</h2>
      <ul>
        <li v-if="reservations.length === 0">None</li>
        <li v-for="reservation in reservations" :key="reservation.room_id + reservation.user">
          {{ reservation.user }}
          {{ reservation.time }}  
          <!--<button @click="removeReservation(room.id)">Remove</button>-->
        </li>
      </ul>
      <input type="text" v-model="newReservationUser" placeholder="Enter your name">
      <input type="datetime-local" v-model="newReservationTime">
      <button @click="reserveRoom(selectedRoom.id,newReservationUser,newReservationTime)">Reserve Room</button>
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
      newReservationUser: '',
      newReservationTime: ''
    }
  },
  mounted() {
    this.fetchRooms();
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
    async removeReservation(roomId) {
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
    async reserveRoom(room,user,time) {
      console.log(time)
      console.log(user)
      console.log(room)
      try {
        const response = await fetch(`http://localhost:8000/rooms/${room}/reserve?user=${user}&time=${time}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
        });

        if (!response.ok) {
          throw new Error('Failed to reserve room');
        }

        this.showReservations(room);
      } catch (error) {
        console.error('Error:', error);
      }
    },
    async listReservations() {
      try {
        const response = await fetch('http://localhost:8000/reservations');
        if (!response.ok) {
          throw new Error('Failed to fetch reservations');
        }
        this.reservations = await response.json();
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
  margin-right: 20px;
}
</style>
