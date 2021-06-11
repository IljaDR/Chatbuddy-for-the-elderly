using UnityEngine;

public class FishManager : MonoBehaviour
{
    public enum Emotion
    {
        anger,
        fear,
        sadness,
        joy,
        neutral
    }

    Rigidbody2D rb;
    SpriteRenderer sr;
    public float speed;
    public Animator animator;
    public Emotion fishEmotion;
    private Vector2 target;
    private Vector2 center = new Vector2(0, 0);
    private float orbitPosition = 270;
    public float radius; 
    public float orbitSpeed;
    private bool happy = false;
    private float multiplier;
    private float distance;
    private float canvasHeight = 8;
    private float canvasWidth = 15;
    public float countdownLength = 0;
    public float emotionCountdown = 10;


    // Start is called before the first frame update
    void Start()
    {
// https://docs.unity3d.com/ScriptReference/Vector2.MoveTowards.html
        rb = GetComponent<Rigidbody2D>();
        sr = GetComponent<SpriteRenderer>();
        fishEmotion = Emotion.neutral;
        target = new Vector2(Random.value * canvasWidth - canvasWidth / 2, Random.value * canvasHeight - canvasHeight / 2);
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        sr.flipX = false;
        countdownLength -= Time.deltaTime;
        emotionCountdown -= Time.deltaTime;

        animator.SetBool("IsSad", false);
        animator.SetBool("IsFear", false);
        animator.SetBool("IsAnger", false);
        animator.SetBool("IsHappy", false);
        animator.SetBool("IsNeutral", false);
        switch (fishEmotion)
        {
            case Emotion.sadness:
                animator.SetBool("IsSad", true);
                happy = false;
                break;
            case Emotion.fear:
                animator.SetBool("IsFear", true);
                happy = false;
                sr.flipX = false;
                break;
            case Emotion.anger:
                animator.SetBool("IsAnger", true);
                happy = false;
                break;
            case Emotion.joy:
                animator.SetBool("IsHappy", true);
                if (!happy)
                {
                    happy = true;
                    orbitPosition = 270;
                }
                break;
            default:
                animator.SetBool("IsNeutral", true);
                happy = false;
                break;
        }

        if(emotionCountdown < 0)
        {
            fishEmotion = Emotion.neutral;
        }

        rb.velocity = new Vector2(speed*Input.GetAxis("Horizontal"), speed*Input.GetAxis("Vertical"));
        if(rb.velocity.x > 0.2)
        {
            sr.flipX = true;
        }
        else if(rb.velocity.x < -0.2)
        {
            sr.flipX = false;
        }

        if(Input.GetAxis("Vertical") < 0.1)
        {
            
            if ((int)(Time.realtimeSinceStartup % 2) == 0)
            {
                rb.velocity = new Vector2(rb.velocity.x, rb.velocity.y + 0.2f);
            }
            else
            {
                rb.velocity = new Vector2(rb.velocity.x, rb.velocity.y - 0.2f);
            }
        }

        if(countdownLength < 0)
        {
            animator.SetBool("Idling", true);
            fishEmotion = Emotion.neutral;
        }
        else
        {
            animator.SetBool("Idling", false);

        }

        if (animator.GetBool("IsHappy"))
        {
            if(Vector2.Distance(rb.position, center) < radius*1.1)
            {
                Vector2 position = new Vector2(radius * Mathf.Cos(Mathf.PI * orbitPosition / 180), radius * Mathf.Sin(Mathf.PI * orbitPosition / 180));
                rb.transform.position = position;

                orbitPosition += orbitSpeed;
                // Someone better versed at maths could probably rewrite this with a fancy sin or cos or something like that
                if (orbitPosition % 360 < 180)
                {
                    sr.flipX = false;
                }
                else
                {
                    sr.flipX = true;
                }
            }
            else
            {
                animator.SetBool("Homing", true);
            }
        }
        animator.SetFloat("Speed", Mathf.Abs(rb.velocity.x));

        if (animator.GetBool("Idling"))
        {
            distance = Vector2.Distance(rb.transform.position, target);
            multiplier = Mathf.Max(distance, 2);
            float step = speed * Time.deltaTime / 5 * multiplier;

            rb.position = Vector2.MoveTowards(rb.position, target, step);
            if (distance < 0.25)
            {
                target = new Vector2(Random.value * canvasWidth - canvasWidth / 2, Random.value * canvasHeight - canvasHeight / 2);
            }
            animator.SetFloat("Speed", 1);
            if(rb.position.x > target.x)
            {
                sr.flipX = false;
            }
            else
            {
                sr.flipX = true;
            } 
        }

        if (!animator.GetBool("Idling") && !animator.GetBool("IsHappy") && Vector2.Distance(rb.transform.position, center) > 0.25 && Mathf.Abs(rb.velocity.x) < 0.5 && Mathf.Abs(rb.velocity.y) < 0.5)
        {
            animator.SetBool("Homing", true);
        }

        if (animator.GetBool("Homing"))
        {
            distance = Vector2.Distance(rb.transform.position, center);
            multiplier = Mathf.Max(distance, 3);
            float step = speed * Time.deltaTime / 5 * multiplier;

            rb.position = Vector2.MoveTowards(rb.position, center, step);
            if (distance < 0.1)
            {
                animator.SetBool("Homing", false);
            }
            animator.SetFloat("Speed", 1);
            if (rb.position.x > center.x)
            {
                sr.flipX = false;
            }
            else
            {
                sr.flipX = true;
            }
        }
    }
}
