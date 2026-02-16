#!/bin/bash
          sudo apt-get install cowsay -y
          /usr/games/cowsay -f dragon "Run for cover, iam a Dragon...RAWR" >> dragon.txt
          grep -i "dragon" dragon.txt 
          cat dragon.txt