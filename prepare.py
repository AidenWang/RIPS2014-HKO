#prepares the actual rainguage data over the forecasted interval
import get_data, multiprocessing, main
 
date_list = main.get_date()
base_dir = main.get_base_dir()
input_list = [date_list, base_dir]
 
pool = multiprocessing.Pool()
pool.map(get_data.prepare_actual, input_list)
