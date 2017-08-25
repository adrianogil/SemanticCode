using TestEngine;
using System.Collections;

namespace Examples.Testbed {
    /// <summary>
    /// Simple test.
    /// </summary>
    public class TestBehaviour : MonoBehaviour  {
        public void Start() {
            /* Testing */
            DebugLogMe('Start');
        }
        public void Update() {
            /* Testing */
            DebugLogMe('Update');
        }
        public void DebugLogMe(string text)
        {
            Debug.Log("TestBehaviour - " + text);
        }
    }
}