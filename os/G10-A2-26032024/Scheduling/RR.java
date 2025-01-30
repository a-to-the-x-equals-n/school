/**
 * RR scheduling algorithm.
 */
 
import java.util.*;

public class RR implements Algorithm
{   
    //Value to allow each task to run for a certain amount of time
    public static final int QUANTUM = 10;

    private List<Task> queue;
    private Task currentTask;

    private int tasksRun;

    public RR(List<Task> queue) {
        this.queue = queue;

        tasksRun = queue.size();
    }

    public void schedule() {
        System.out.println("RR Scheduling \n");

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
        return queue.get(0);
    }
}
