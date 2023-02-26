<template>
  <div class="">
    
    <nav class="bg-slate-200 border-gray-200 px-2 sm:px-4 py-2.5 dark:bg-gray-900">
      <div class="container flex flex-wrap items-center justify-between mx-auto">
        <a class="flex items-center">
            <img src="./assets/chessLogo.png" class="h-6 mr-3 sm:h-9" alt="Flowbite Logo" />
        </a>
        <button data-collapse-toggle="navbar-default" type="button" class="inline-flex items-center p-2 ml-3 text-sm text-gray-500 rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600" aria-controls="navbar-default" aria-expanded="false">
          <span class="sr-only">Open main menu</span>
          <svg class="w-6 h-6" aria-hidden="true" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"></path></svg>
        </button>
        <div class="hidden w-full md:block md:w-auto" id="navbar-default">
          <ul class="flex flex-col p-4 mt-4 border border-gray-100 rounded-lg bg-gray-50 md:flex-row md:space-x-8 md:mt-0 md:text-sm md:font-medium md:border-0 md:bg-white dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700">
            <li>
              <button @click="viewSwap('home')" class="block py-2 pl-3 pr-4 text-gray-700 rounded hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-gray-400 md:dark:hover:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent">Home</button>
            </li>
            <li>
              <button @click="viewSwap('play')" class="block py-2 pl-3 pr-4 text-gray-700 rounded hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-gray-400 md:dark:hover:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent">Play</button>
            </li>
            <li>
              <button @click="viewSwap('about')" class="block py-2 pl-3 pr-4 text-gray-700 rounded hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-gray-400 md:dark:hover:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent">About Us</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <section id="home" v-if="page === 'home'">
      <div class="grid max-w-screen-xl px-4 py-8 mx-auto lg:gap-8 xl:gap-0 lg:py-16 lg:grid-cols-12">
        <div class="mr-auto place-self-center lg:col-span-7">
            <h1 class="max-w-2xl mb-4 text-4xl font-extrabold leading-none tracking-tight md:text-5xl xl:text-6xl dark:text-white">Welcome to ChessWesTX</h1>
            <p class="max-w-2xl mb-6 font-light text-gray-500 lg:mb-8 md:text-lg lg:text-xl dark:text-gray-400">Also known as Not Chess.com</p>
            <button @click="viewSwap('play')" class="inline-flex items-center justify-center px-5 py-3 mr-3 text-base font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 dark:focus:ring-blue-900">
                Play Now
                <svg class="w-5 h-5 ml-2 -mr-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
            </button>
            <button @click="viewSwap('about')" class="inline-flex items-center justify-center px-5 py-3 text-base font-medium text-center text-gray-900 border border-gray-300 rounded-lg hover:bg-gray-100 dark:text-white dark:border-gray-700 dark:hover:bg-gray-700 ">
                About the Creators
            </button> 
        </div>
        <div class="hidden lg:mt-0 lg:col-span-5 lg:flex">
            <img src="https://www.dailychess.com/img/uibit/home/chess-board-opening.png" alt="mockup">
        </div>                
      </div>
    </section>
    <section v-if="page === 'play'">
      <h1 class="max-w-2xl mb-4 text-4xl font-extrabold leading-none tracking-tight md:text-5xl xl:text-6xl dark:text-white text-center my-8 mx-auto">
        Start Game
      </h1>
      <p class="max-w-2x1 font-light text-gray-500 lg:mb-8 md:text-lg lg:text-xl dark:text-gray-400 text-center mb-12">
        Choose how you would like to play:
      </p>
      
      <div class="mx-32 columns-2 mt-2 gap-10">
        <div>
          <p class="max-w-2x1 font-light text-gray-500 md:text-lg lg:text-xl dark:text-gray-400 text-center mb-3">
            Player Count
          </p>
          
<div class="mb-5 flex items-center pl-4 border border-gray-200 rounded dark:border-gray-700">
    <input @select="setPlayers(2)" checked id="player-radio-1" type="radio" value="" name="players-radio" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
    <label for="player-radio-1" class="w-full py-4 ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">Two Players</label>
</div>
<div class="flex items-center pl-4 border border-gray-200 rounded dark:border-gray-700">
    <input @select="setPlayers(1)" id="player-radio-2" type="radio" value="" name="players-radio" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
    <label for="player-radio-2" class="w-full py-4 ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">One Player with AI</label>
</div>

        </div>
        <div>

          <p class="max-w-2x1 font-light text-gray-500 md:text-lg lg:text-xl dark:text-gray-400 text-center mb-3">
            Input type
          </p>

          <div class="mb-5 flex items-center pl-4 border border-gray-200 rounded dark:border-gray-700">
    <input @click="setInput(1)" checked id="input-radio-1" type="radio" value="" name="bordered-radio" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
    <label for="input-radio-1" class="w-full py-4 ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">Keyboard Controls</label>
</div>
<div class="flex items-center pl-4 border border-gray-200 rounded dark:border-gray-700">
    <input @click="setInput(2)" id="input-radio-2" type="radio" value="" name="bordered-radio" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
    <label for="input-radio-2" class="w-full py-4 ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">Voice Controls</label>
</div>


        </div>
      </div>
      <div class="flex mt-5">
        <button @click="startGame()" type="button" class="mx-auto text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800">Start Game</button>
      </div>


      

    </section>



    <section v-if="page === 'start'">

      <h1 class="max-w-2xl mb-4 text-4xl font-extrabold leading-none tracking-tight md:text-5xl xl:text-6xl dark:text-white text-center my-8 mx-auto">
        {{ curPlayer }} to move
      </h1>
      <img id="boardImg" @click="swapPlayers()" class="max-w-lg mx-auto mt-4" src="./assets/temp.svg" alt="">

 <div class="mt-4 max-w-md mx-auto">
      <div v-if="inputType.valueOf() === 1" class="mb-6">
    <label for="from-input" class="text-center block mb-2 text-sm font-medium text-gray-900 dark:text-white">Enter a Piece Coordinate</label>
    <input v-model="fromInput" type="text" id="from-input" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
</div>

<div v-if="inputType.valueOf() === 1" class="mb-6">
    <label for="to-input" class="text-center block mb-2 text-sm font-medium text-gray-900 dark:text-white">Enter a Coordinate to Move it to</label>
    <input v-model="toInput" type="text" id="to-input" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
</div>

<div v-if="inputType.valueOf() === 1" class="flex mt-5">
        <button @click="sendMove(fromInput, toInput)" type="button" class="mx-auto text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800">Send Move</button>
      </div>
  </div>
    </section>



    <section v-if="page === 'about'">
      <h1 class="max-w-2xl mb-4 text-4xl font-extrabold leading-none tracking-tight md:text-5xl xl:text-6xl dark:text-white text-center my-8 mx-auto">
        About Us
      </h1>
      <p class="max-w-2x1 font-light text-gray-500 lg:mb-8 md:text-lg lg:text-xl dark:text-gray-400 text-center mb-12">
        Learn more about the people behind ChessWesTX
      </p>
    </section>
  </div>
  
</template>

<script lang="ts" setup>
  import { ref } from 'vue';

  const page = ref("home");
  const players = ref(2);
  const inputType = ref(1);
  const toInput = "";
  const fromInput = "";
  const curPlayer = ref("White");

  // For swapping between each page view
  const viewSwap = (view: string) => {
    if(view === "play"){
      setPlayers(2);
      setInput(1);
    }
    page.value = view;
  }
  const setPlayers = (num: number) => {
    players.value = num;
  }  
  const setInput = (type: number) => {
    inputType.value = type;
  }
  const startGame = () => {

    curPlayer.value = 'White';
    page.value = 'start';
  }

  const swapPlayers = () => {
    if(curPlayer.value === "White"){
      curPlayer.value = "Black";
    } else {
      curPlayer.value = "White"
    }
  }
  const sendMove = (from: string, to: string) => {
    const totalMove = from + to;
    console.log(totalMove);
  }
</script>