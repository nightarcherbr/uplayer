import time;
import sys;
import logging;
sys.path.append(".");

from gi.repository import Gtk;

import core.player;
import core.watchdog;
import core.log;
import threading;

try:
	# Iniciando o sistema de watchdog
	core.watchdog.start();

	# Inicializa o log
	core.log.start();
	logging.info("Inicializando o player");

	# Inicia o processo de scheduler
	logging.info("Inicializando o agendamento de tarefas");
	core.player.start_scheduler();

	# Cria o model
	logging.info("Inicializando a playlist");
	core.player.create_model();

	# Cria o workspace
	logging.info("Inicializando a interface grafica");
	workspace = core.player.get_window();

	
	Gtk.main();
except Exception as ex:
	logging.exception(ex);