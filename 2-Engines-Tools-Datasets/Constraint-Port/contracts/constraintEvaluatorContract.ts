/**
 * Constraint Port — Evaluator Contract
 * Interface definitions for the constraint evaluation pipeline.
 * Types/interfaces only. No runtime code.
 *
 * Authority: L0-CMD-CONOS-VKGL04R-CPORT-001
 */

import type {
  ConstraintObject,
  ConstraintEvidence,
  ConstraintDecision,
  DecisionAction,
  Severity,
} from "./constraintTypes";

/**
 * Input to the constraint evaluator.
 * Contains the rule to evaluate and the context for evaluation.
 */
export interface ConstraintEvaluationInput {
  /** The constraint rule to evaluate */
  constraint: ConstraintObject;

  /** Evidence collected for this evaluation */
  evidence: ConstraintEvidence;

  /** Evaluation context: project, scope, and entity data */
  context: EvaluationContext;
}

/**
 * Context data required for constraint evaluation.
 */
export interface EvaluationContext {
  /** Project identifier */
  project_id: string;

  /** Scope boundary identifier */
  scope_id: string;

  /** The specific entities being evaluated */
  target_entities: TargetEntity[];

  /** Timestamp of the evaluation request */
  evaluation_timestamp: string;
}

/**
 * A specific entity being evaluated against constraints.
 */
export interface TargetEntity {
  entity_id: string;
  entity_type: string;
  properties: Record<string, unknown>;
}

/**
 * Output from the constraint evaluator.
 * Always deterministic. Always includes evidence reference.
 */
export interface ConstraintEvaluationOutput {
  /** The structured decision */
  decision: ConstraintDecision;

  /** Whether all dependencies were resolvable */
  dependencies_resolved: boolean;

  /** List of any unresolvable dependencies */
  unresolved_dependencies?: string[];

  /** Evaluation trace for audit */
  evaluation_trace: EvaluationTraceEntry[];
}

/**
 * A single step in the evaluation trace for auditing.
 */
export interface EvaluationTraceEntry {
  step: number;
  action: string;
  input_ref: string;
  result: string;
  timestamp: string;
}

/**
 * Contract for the Constraint Evaluator.
 *
 * Evaluation order is deterministic:
 * 1. Validate input completeness
 * 2. Resolve dependencies from dependency_map
 * 3. Check evidence completeness
 * 4. If evidence is MISSING or PARTIAL → apply decision_on_fail
 * 5. If evidence is COMPLETE → evaluate trigger condition
 * 6. Produce decision with full evidence chain
 *
 * Fail-closed rule:
 * - Missing evidence → BLOCK (unless decision_on_fail specifies otherwise)
 * - Unresolvable dependency → BLOCK
 * - Non-deterministic state → BLOCK
 */
export interface IConstraintEvaluator {
  /**
   * Evaluate a single constraint against provided evidence and context.
   * Must be deterministic: same inputs always produce same output.
   */
  evaluate(input: ConstraintEvaluationInput): ConstraintEvaluationOutput;
}

/**
 * Contract for batch evaluation of multiple constraints.
 *
 * Evaluation order: constraints are evaluated in rule_id sort order
 * to ensure deterministic sequencing. No parallel evaluation.
 */
export interface IConstraintBatchEvaluator {
  /**
   * Evaluate multiple constraints sequentially in deterministic order.
   * Returns one output per input constraint.
   */
  evaluateBatch(
    inputs: ConstraintEvaluationInput[]
  ): ConstraintEvaluationOutput[];

  /**
   * Returns the aggregate action: the most severe action from all results.
   * Severity order: BLOCK > REQUIRE_HUMAN_STAMP > DEFER > WARN > PASS
   */
  aggregateAction(
    outputs: ConstraintEvaluationOutput[]
  ): DecisionAction;

  /**
   * Returns the highest severity from all results.
   * Severity order: CRITICAL > HIGH > MEDIUM > LOW > INFO
   */
  aggregateSeverity(
    outputs: ConstraintEvaluationOutput[]
  ): Severity;
}
