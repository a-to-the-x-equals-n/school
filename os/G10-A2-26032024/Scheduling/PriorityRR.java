/**
 * Priority RR scheduling algorithm.
 */
 
import java.util.*;

public class PriorityRR implements Algorithm
{   public static final int QUANTUM = 10;
    private List<Task> queue;
    private Task currentTask;

    private int tasksRun;

    public PriorityRR(List<Task> queue) {
        this.queue = queue;

        tasksRun = queue.size();
    }

    public void schedule() {
        System.out.println("PriorityRR Scheduling \n");

        while (!queue.isEmpty()) {
            currentTask = pickNextTask();

            //Burst value of current Task
            int currBurst = currentTask.getBurst();

            CPU.run(currentTask, currBurst);

            //Remove task from queue
            queue.remove(currentTask);

            //If task burst value is higher than the QUANTUM
            //Add task back into queue to run again for the QUANTUM time
            if(currBurst > QUANTUM) {
                currentTask.setBurst(currBurst - QUANTUM);
                queue.add(currentTask);
                System.out.println("Rescheduling " + currentTask.getName() + "\n" + "Time remaining: " + currentTask.getBurst()+ "\n");
            }

            else System.out.println("Finished running " + currentTask.getName() + "\n");


        }
    }

    public Task pickNextTask() {
        //Holds task with highest priority
        //Puts first task in queue in highPri
        Task highPri = (Task)this.queue.get(0);
        
        //Highest priority value
        int pri = highPri.getPriority();

        //Loop through task queue
        for(int i = 1; i < queue.size(); i++) {

            //Current task
            Task curr = (Task)this.queue.get(i);
            //Priority of current task
            int currPri = curr.getPriority();

            //If priority of current task is higher than highest priority encountered
            //change highest priority task to current task
            if(currPri > pri) {
                pri = currPri;
                highPri = curr;
            }
        }

        //Return the highest priority
        return highPri;
    }
}
