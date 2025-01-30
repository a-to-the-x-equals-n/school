/**
 * SJF scheduling algorithm.
 */
 
import java.util.*;

public class SJF implements Algorithm
{
    private List<Task> queue;
    private Task currentTask;

    private int tasksRun;

    public SJF(List<Task> queue) {
        this.queue = queue;

        tasksRun = queue.size();
    }

    public void schedule() {
        System.out.println("SJF Scheduling \n");

        while (!queue.isEmpty()) {
            currentTask = pickNextTask();
            
            CPU.run(currentTask, currentTask.getBurst());

            // remove the task
            queue.remove(currentTask);
        }
    }

    public Task pickNextTask() {

        //Holds the shortest task
        //Puts first task in queue into shrt
        Task shrt = (Task)this.queue.get(0);

        //Shortest burst value
        int burst = shrt.getBurst();

        //Loop through queue
        for(int i = 1; i < queue.size(); i++) {

            //Current task
            Task curr = (Task)this.queue.get(i);
            //Burst of current task
            int currBurst = curr.getBurst();

            //If the current burst is smaller than the shortest burst encountered change shortest task
            //and burst of shortest task
            if(currBurst < burst) {
                burst = currBurst;
                shrt = curr;
            }
        }

        //Return the shortest task
        return shrt;
    }
}
