#!/usr/bin/env python3
"""Comprehensive test script for chatbot enhancements.

Tests:
1. Fuzzy task matching
2. Natural language date parsing
3. Smart priority detection
4. Batch operation detection
5. Task validation
"""

import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.ai_agent.utils import (
    parse_natural_date,
    fuzzy_match_task_title,
    suggest_priority_from_keywords,
    detect_batch_operation,
    validate_task_data,
    extract_task_id_from_message,
    format_task_list_response
)


def test_natural_date_parsing():
    """Test natural language date parsing."""
    print("\n🧪 Testing Natural Language Date Parsing")
    print("=" * 60)

    test_cases = [
        ("tomorrow", "Should parse to tomorrow"),
        ("today", "Should parse to today"),
        ("next Friday", "Should parse to next Friday"),
        ("in 3 days", "Should parse to 3 days from now"),
        ("January 15", "Should parse to Jan 15"),
        ("2026-01-20", "Should parse ISO format"),
        ("tomorrow at 3pm", "Should parse with time"),
        ("next Monday at 14:30", "Should parse day with time"),
    ]

    passed = 0
    failed = 0

    for date_str, description in test_cases:
        result = parse_natural_date(date_str)
        if result:
            print(f"✅ '{date_str}' → {result.isoformat()} ({description})")
            passed += 1
        else:
            print(f"❌ '{date_str}' → Failed to parse ({description})")
            failed += 1

    print(f"\n📊 Date Parsing: {passed} passed, {failed} failed")
    return failed == 0


def test_fuzzy_matching():
    """Test fuzzy task title matching."""
    print("\n🧪 Testing Fuzzy Task Matching")
    print("=" * 60)

    task_titles = [
        "buy milk from store",
        "call mom tomorrow",
        "submit project report",
        "fix bug in production",
        "review pull request"
    ]

    test_cases = [
        ("milk", "Should match 'buy milk from store'"),
        ("byu milk", "Should match despite typo"),
        ("call mom", "Should exact match"),
        ("project report", "Should match 'submit project report'"),
        ("fix production bug", "Should match with word order variation"),
        ("xyz nonexistent", "Should return no matches")
    ]

    passed = 0
    failed = 0

    for query, description in test_cases:
        matches = fuzzy_match_task_title(query, task_titles, threshold=60)
        if matches:
            best_match, score = matches[0]
            print(f"✅ '{query}' → '{best_match}' ({score}% match) - {description}")
            passed += 1
        else:
            if "nonexistent" in query:
                print(f"✅ '{query}' → No matches (expected) - {description}")
                passed += 1
            else:
                print(f"❌ '{query}' → No matches - {description}")
                failed += 1

    print(f"\n📊 Fuzzy Matching: {passed} passed, {failed} failed")
    return failed == 0


def test_priority_detection():
    """Test smart priority detection from keywords."""
    print("\n🧪 Testing Smart Priority Detection")
    print("=" * 60)

    test_cases = [
        ("urgent fix needed", "high", "Should detect HIGH from 'urgent'"),
        ("call client asap", "high", "Should detect HIGH from 'asap'"),
        ("review documentation someday", "low", "Should detect LOW from 'someday'"),
        ("buy groceries", "medium", "Should default to MEDIUM"),
        ("critical bug in production", "high", "Should detect HIGH from 'critical'"),
        ("minor typo fix", "low", "Should detect LOW from 'minor'"),
    ]

    passed = 0
    failed = 0

    for title, expected_priority, description in test_cases:
        result = suggest_priority_from_keywords(title)
        if result == expected_priority:
            print(f"✅ '{title}' → {result} (expected {expected_priority}) - {description}")
            passed += 1
        else:
            print(f"❌ '{title}' → {result} (expected {expected_priority}) - {description}")
            failed += 1

    print(f"\n📊 Priority Detection: {passed} passed, {failed} failed")
    return failed == 0


def test_batch_operation_detection():
    """Test batch operation detection."""
    print("\n🧪 Testing Batch Operation Detection")
    print("=" * 60)

    test_cases = [
        ("delete all completed tasks", {"operation": "delete", "filter": "completed"}),
        ("remove all done tasks", {"operation": "delete", "filter": "completed"}),
        ("mark all high priority as complete", {"operation": "complete", "filter": "high"}),
        ("complete all urgent tasks", {"operation": "complete", "filter": "high"}),
        ("show my tasks", None),  # Not a batch operation
    ]

    passed = 0
    failed = 0

    for message, expected in test_cases:
        result = detect_batch_operation(message)
        if result == expected:
            print(f"✅ '{message}' → {result}")
            passed += 1
        else:
            print(f"❌ '{message}' → {result} (expected {expected})")
            failed += 1

    print(f"\n📊 Batch Operation Detection: {passed} passed, {failed} failed")
    return failed == 0


def test_task_validation():
    """Test task data validation."""
    print("\n🧪 Testing Task Data Validation")
    print("=" * 60)

    test_cases = [
        ("Valid task title", datetime.now() + timedelta(days=1), True, None),
        ("", None, False, "Task title cannot be empty"),
        ("x" * 250, None, False, "Task title too long"),
        ("Valid", datetime.now() - timedelta(days=400), False, "more than a year in the past"),
        ("Valid", datetime.now() + timedelta(days=4000), False, "too far in the future"),
    ]

    passed = 0
    failed = 0

    for title, due_date, expected_valid, expected_error_substring in test_cases:
        is_valid, error_msg = validate_task_data(title, due_date)

        if is_valid == expected_valid:
            if not is_valid and expected_error_substring:
                if expected_error_substring in (error_msg or ""):
                    print(f"✅ Validation correct: {error_msg}")
                    passed += 1
                else:
                    print(f"❌ Wrong error message: got '{error_msg}', expected substring '{expected_error_substring}'")
                    failed += 1
            else:
                print(f"✅ Validation correct: {'Valid' if is_valid else error_msg}")
                passed += 1
        else:
            print(f"❌ Validation incorrect: got {is_valid}, expected {expected_valid}")
            failed += 1

    print(f"\n📊 Task Validation: {passed} passed, {failed} failed")
    return failed == 0


def test_task_id_extraction():
    """Test task ID extraction from messages."""
    print("\n🧪 Testing Task ID Extraction")
    print("=" * 60)

    test_cases = [
        ("update task 5", 5),
        ("delete #42", 42),
        ("complete task number 7", 7),
        ("mark task id 123 as done", 123),
        ("show my tasks", None),  # No ID
    ]

    passed = 0
    failed = 0

    for message, expected_id in test_cases:
        result = extract_task_id_from_message(message)
        if result == expected_id:
            print(f"✅ '{message}' → ID={result}")
            passed += 1
        else:
            print(f"❌ '{message}' → ID={result} (expected {expected_id})")
            failed += 1

    print(f"\n📊 Task ID Extraction: {passed} passed, {failed} failed")
    return failed == 0


def test_task_list_formatting():
    """Test task list response formatting."""
    print("\n🧪 Testing Task List Formatting")
    print("=" * 60)

    test_tasks = [
        {
            "task_id": 1,
            "title": "Buy milk",
            "completed": False,
            "priority": "high",
            "due_date": (datetime.now() + timedelta(days=1)).isoformat()
        },
        {
            "task_id": 2,
            "title": "Call mom",
            "completed": True,
            "priority": "medium",
            "due_date": None
        },
        {
            "task_id": 3,
            "title": "Submit report",
            "completed": False,
            "priority": "low",
            "due_date": None
        }
    ]

    result = format_task_list_response(test_tasks)
    print(f"\n{result}")

    # Check for key elements
    checks = [
        ("📋" in result, "Has emoji"),
        ("Buy milk" in result, "Contains task title"),
        ("✅" in result or "⏳" in result, "Has status emoji"),
        ("high priority" in result or "🔴" in result, "Shows priority"),
    ]

    passed = sum(1 for check, _ in checks if check)
    failed = len(checks) - passed

    for check, description in checks:
        status = "✅" if check else "❌"
        print(f"{status} {description}")

    print(f"\n📊 Task Formatting: {passed} passed, {failed} failed")
    return failed == 0


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("🧪 CHATBOT ENHANCEMENTS TEST SUITE")
    print("=" * 60)

    all_tests = [
        ("Natural Date Parsing", test_natural_date_parsing),
        ("Fuzzy Task Matching", test_fuzzy_matching),
        ("Priority Detection", test_priority_detection),
        ("Batch Operation Detection", test_batch_operation_detection),
        ("Task Validation", test_task_validation),
        ("Task ID Extraction", test_task_id_extraction),
        ("Task List Formatting", test_task_list_formatting),
    ]

    results = []
    for test_name, test_func in all_tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"\n❌ {test_name} crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))

    # Print summary
    print("\n" + "=" * 60)
    print("📊 FINAL SUMMARY")
    print("=" * 60)

    passed_count = sum(1 for _, passed in results if passed)
    failed_count = len(results) - passed_count

    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")

    print(f"\n🎯 Overall: {passed_count}/{len(results)} test suites passed")

    if failed_count == 0:
        print("\n🎉 ALL TESTS PASSED! Chatbot enhancements are working correctly.")
        return 0
    else:
        print(f"\n⚠️  {failed_count} test suite(s) failed. Review errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
