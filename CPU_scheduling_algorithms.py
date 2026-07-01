
class SchedulingAlgorithms:
    @staticmethod
    def simulate_fcfs(processes):
        procs = sorted(processes, key=lambda x: x['at'])
        current_time = 0
        schedule = []
        total_tat = 0
        total_wt = 0

        for p in procs:
            if current_time < p['at']:
                current_time = p['at'] 
            
            start_time = current_time
            current_time += p['bt']
            
            tat = current_time - p['at']
            wt = tat - p['bt']
            
            total_tat += tat
            total_wt += wt
            
            schedule.append((p['name'], start_time, current_time))

        num_of_processes = len(procs)
        return schedule, total_tat / num_of_processes, total_wt / num_of_processes

    @staticmethod
    def simulate_rr(processes, tq):
        procs = sorted(processes, key=lambda x: x['at'])
        num_of_processes = len(procs)
        current_time = 0
        schedule = []
        completed = 0
        completion_times = {}
        ready_queue = []
        idx = 0

        while idx < num_of_processes and procs[idx]['at'] <= current_time:
            ready_queue.append(procs[idx])
            idx += 1

        if not ready_queue and idx < num_of_processes:
            current_time = procs[idx]['at']
            ready_queue.append(procs[idx])
            idx += 1

        while completed < num_of_processes:
            if not ready_queue:
                current_time = procs[idx]['at']
                while idx < num_of_processes and procs[idx]['at'] <= current_time:
                    ready_queue.append(procs[idx])
                    idx += 1

            p = ready_queue.pop(0)
            start_time = current_time
            
            time_processed = min(p['rem_bt'], tq)
            p['rem_bt'] -= time_processed
            current_time += time_processed
            
            schedule.append((p['name'], start_time, current_time))

            while idx < num_of_processes and procs[idx]['at'] <= current_time:
                ready_queue.append(procs[idx])
                idx += 1

            if p['rem_bt'] > 0:
                ready_queue.append(p)
            else:
                completed += 1
                completion_times[p['name']] = current_time

        total_tat = 0
        total_wt = 0
        for p in processes:
            tat = completion_times[p['name']] - p['at']
            wt = tat - p['bt']
            total_tat += tat
            total_wt += wt

        return schedule, total_tat / num_of_processes, total_wt / num_of_processes
    
    @staticmethod
    def simulate_sjf(processes):
        num_of_processes = len(processes)
        completed = 0
        current_time = 0
        schedule = []
        total_tat = 0
        total_wt = 0
        
        is_completed = {p['name']: False for p in processes}
        
        while completed < num_of_processes:
            available = [p for p in processes if p['at'] <= current_time and not is_completed[p['name']]]
            
            if not available:
                next_arrival = min([p['at'] for p in processes if not is_completed[p['name']]])
                current_time = next_arrival
                continue
            
            available.sort(key=lambda x: (x['bt'], x['at']))
            p = available[0] 
            
            start_time = current_time
            current_time += p['bt']
            is_completed[p['name']] = True
            completed += 1
            
            tat = current_time - p['at']
            wt = tat - p['bt']
            total_tat += tat
            total_wt += wt
            
            schedule.append((p['name'], start_time, current_time))
            
        return schedule, total_tat / num_of_processes, total_wt / num_of_processes

    @staticmethod
    def simulate_srtf(processes):
        num_of_processes = len(processes)
        completed = 0
        current_time = 0
        schedule = []
        total_tat = 0
        total_wt = 0
        
        completion_times = {}
        current_process = None
        block_start_time = 0
        
        while completed < num_of_processes:
            available = [p for p in processes if p['at'] <= current_time and p['rem_bt'] > 0]
            
            if not available:
                if current_process is not None:
                    schedule.append((current_process, block_start_time, current_time))
                    current_process = None
                
                next_arrival = min([p['at'] for p in processes if p['rem_bt'] > 0])
                current_time = max(current_time + 1, next_arrival)
                continue
            
            available.sort(key=lambda x: (x['rem_bt'], x['at']))
            shortest = available[0]
            
            if current_process != shortest['name']:
                if current_process is not None:
                    schedule.append((current_process, block_start_time, current_time))
                
                current_process = shortest['name']
                block_start_time = current_time
            
            shortest['rem_bt'] -= 1
            current_time += 1
            
            if shortest['rem_bt'] == 0:
                completed += 1
                completion_times[shortest['name']] = current_time
                
                schedule.append((current_process, block_start_time, current_time))
                current_process = None 

        for p in processes:
            tat = completion_times[p['name']] - p['at']
            wt = tat - p['bt']
            total_tat += tat
            total_wt += wt

        return schedule, total_tat / num_of_processes, total_wt / num_of_processes
    
    @staticmethod
    def simulate_priority_nonpreemptive(processes):
        n = len(processes)
        completed = 0
        current_time = 0
        schedule = []
        total_tat = 0
        total_wt = 0
        
        is_completed = {p['name']: False for p in processes}
        
        while completed < n:
            available = [p for p in processes if p['at'] <= current_time and not is_completed[p['name']]]
            
            if not available:
                next_arrival = min([p['at'] for p in processes if not is_completed[p['name']]])
                current_time = next_arrival
                continue
            
            available.sort(key=lambda x: (x['pr'], x['at']))
            p = available[0] 
            
            start_time = current_time
            current_time += p['bt']
            is_completed[p['name']] = True
            completed += 1
            
            tat = current_time - p['at']
            wt = tat - p['bt']
            total_tat += tat
            total_wt += wt
            
            schedule.append((p['name'], start_time, current_time))
            
        return schedule, total_tat / n, total_wt / n
    
    @staticmethod
    def simulate_priority_preemptive(processes):
        n = len(processes)
        completed = 0
        current_time = 0
        schedule = []
        total_tat = 0
        total_wt = 0
        
        completion_times = {}
        current_process = None
        block_start_time = 0
        
        while completed < n:
            available = [p for p in processes if p['at'] <= current_time and p['rem_bt'] > 0]
            
            if not available:
                if current_process is not None:
                    schedule.append((current_process, block_start_time, current_time))
                    current_process = None
                
                next_arrival = min([p['at'] for p in processes if p['rem_bt'] > 0])
                current_time = max(current_time + 1, next_arrival)
                continue
            
            available.sort(key=lambda x: (x['pr'], x['at']))
            highest_priority = available[0]
            
            if current_process != highest_priority['name']:
                if current_process is not None:
                    schedule.append((current_process, block_start_time, current_time))
                
                current_process = highest_priority['name']
                block_start_time = current_time
            
            highest_priority['rem_bt'] -= 1
            current_time += 1
            
            if highest_priority['rem_bt'] == 0:
                completed += 1
                completion_times[highest_priority['name']] = current_time
                
                schedule.append((current_process, block_start_time, current_time))
                current_process = None 

        for p in processes:
            tat = completion_times[p['name']] - p['at']
            wt = tat - p['bt']
            total_tat += tat
            total_wt += wt

        return schedule, total_tat / n, total_wt / n